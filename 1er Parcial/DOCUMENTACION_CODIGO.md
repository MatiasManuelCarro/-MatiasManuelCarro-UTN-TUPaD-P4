# 📦 FoodStore — Modelo de Productos  
README técnico con todas las decisiones tomadas hasta ahora

Este documento resume todas las decisiones de diseño, validaciones de dominio, justificaciones UML y reglas del PDF aplicadas al código actual del modelo de productos.

---

# 🧩 DomainError

```python
class DomainError(ValueError):
    pass
```

Motivo:
- El PDF exige “excepción de dominio” para reglas inválidas.
- Hereda de ValueError porque representa datos incorrectos del usuario o del negocio.
- Se usa en todas las validaciones específicas de cada tipo de producto.

---

# 🧩 UnidadMedida (Value Object)

```python
@dataclass(frozen=True)
class UnidadMedida:
    nombre: str
    simbolo: str
    tipo: str
```

Motivo:
- Es un Value Object: inmutable (frozen=True).
- Representa la unidad de venta (kg, g, L, unidad, etc.).
- No tiene lógica, solo datos.

---

# 🧩 Categoria (Entidad simple)

```python
class Categoria:
    def __init__(self, nombre: str, descripcion: str = "") -> None:
        if not nombre.strip():
            raise DomainError("El nombre de la categoría no puede estar vacío")
        self._nombre = nombre.strip()
        self._descripcion = descripcion
```

Motivo:
- El nombre no puede ser vacío → regla del dominio.
- Atributos privados + properties → inmutabilidad lógica.
- No tiene setters: una categoría no cambia una vez creada.

---

# 🧩 ProductoCategoria (Composición)

```python
class ProductoCategoria:
    def __init__(self, producto: Producto, categoria: Categoria, es_principal: bool = False):
        self._producto = producto
        self._categoria = categoria
        self._es_principal = es_principal
```

Motivo:
- Representa la composición Producto → ProductoCategoria.
- Cada producto crea su clasificación principal automáticamente.
- es_principal indica la categoría principal del producto.

---

# 🧩 Producto (Clase abstracta — contrato del dominio)

```python
class Producto(ABC):
    @abstractmethod
    def precio_final(self, cantidad: float) -> float:
        raise NotImplementedError
```

Motivo:
- Es abstracta: no se instancia nunca.
- Define el contrato del dominio: todas las subclases deben implementar precio_final.
- Contiene el estado común de cualquier producto:
  - nombre
  - precio_base
  - stock
  - unidad_venta
  - habilitado
  - categorías (composición)

Por qué las subclases llaman a super():
- Producto inicializa todo el estado común.
- Producto crea la clasificación principal.
- Las subclases no redefinen el dominio, solo agregan reglas específicas.

---

# 🧩 ProductoSimple (se vende por unidad)

```python
class ProductoSimple(Producto):
    def __init__(...):
        if precio_base < 1 or precio_base != int(precio_base):
            raise DomainError("precio_base debe ser entero y no puede ser negativo en ProductoSimple")
        super().__init__(...)

    def precio_final(self, cantidad: float) -> float:
        return self._precio_base * cantidad
```

Reglas del PDF:
- Se vende por pieza/unidad.
- precio_base debe ser entero y >= 1.
  - 3 → válido
  - 3.0 → válido
  - 2.5 → inválido
- Si no cumple → DomainError.
- El cálculo es: precio_final = precio_base × cantidad
- No redondea (solo ProductoPorPeso lo hace).

---

# 🧩 ProductoPorPeso (se vende por peso/volumen)

```python
class ProductoPorPeso(Producto):
    def __init__(...):
        if precio_base <= 0:
            raise DomainError("precio_base debe ser > 0 para ProductoPorPeso")
        super().__init__(...)

    def precio_final(self, cantidad: float) -> float:
        return round(self._precio_base * cantidad, 2)
```

Reglas del PDF:
- Se vende por peso o volumen (kg, g, L, ml).
- precio_base debe ser > 0.
- Admite decimales (ej: 8500.50 por kg).
- El cálculo es: precio_final = precio_base × cantidad
- Solo esta subclase redondea → round(..., 2).

---

# 🍕 ProductoCombo — Diseño, decisiones y justificación completa

`ProductoCombo` es la tercera subclase concreta de `Producto` en el catálogo de Food Store.  
Representa un **producto del catálogo** que agrupa otros productos ya existentes y aplica un descuento sobre la suma de sus precios.

Este README explica **todas las decisiones de diseño**, **por qué se tomaron**, y **cómo se justifican** según el PDF del parcial, el UML y el criterio de dominio.


## 🧩 1. Rol en el dominio

Un combo **es-un Producto** del catálogo.  
Por lo tanto:

- aparece en el menú,
- tiene nombre propio,
- tiene categoría principal,
- tiene stock propio,
- puede estar habilitado o deshabilitado,
- tiene precio publicado,
- se exporta al punto de venta igual que cualquier producto.

Los productos que agrupa **no desaparecen** ni cambian su ciclo de vida:  
esto es **agregación**, no composición.



## 🧩 2. Constructor y parámetros

```python
class ProductoCombo(Producto):
    def __init__(
        self,
        nombre: str,
        componentes: list[Producto],
        descuento: float,
        precio_base: float,
        stock_cantidad: float,
        unidad_venta: UnidadMedida | None,
        categoria_principal: Categoria,
        habilitado: bool = True,
    ) -> None:
```

A continuación se explica **por qué** el combo recibe cada uno de estos parámetros.



## ✔ nombre: str  
El combo es un **Producto del catálogo**, por lo tanto tiene nombre propio.  
Ejemplos reales: “Combo Almuerzo”, “Combo Familiar”.



## ✔ componentes: list[Producto]  
Los componentes:

- **se reciben ya construidos**,  
- **existen antes y después del combo**,  
- pueden ser **ProductoSimple**, **ProductoPorPeso** o **ProductoCombo** (combos anidados).

Esto cumple exactamente el PDF:

> “Agregación — ProductoCombo y sus componentes (1 a 2..*).  
> Se reciben ya construidos y existen antes y después del combo.”



## ✔ descuento: float  
El descuento es **propiedad del combo**, no de los componentes.

Regla del PDF:

> “El descuento se fija al construir y debe estar en [0, 1).”


## ✔ precio_base: float  
### **Decisión tomada (correcta y defendible):**  
**El precio_base del combo se recibe como dato de catálogo.  
No se deriva de los componentes.  
No participa del cálculo del precio final.**

¿Por qué?

1. Producto exige tener `precio_base` y mostrar `precio_publicado`.  
2. El cálculo del combo **NO usa precio_base**, usa `precio_final(1)` de cada componente.  
3. precio_base del combo es un **precio de referencia** para el catálogo.

PDF:

> “Decidí si lo recibís como dato de catálogo o lo derivás de sus componentes,  
> e implementalo de forma coherente con precio_publicado.”



## ✔ stock_cantidad: float  
### **Decisión tomada (correcta y defendible):**  
**El combo tiene stock propio.  
No depende del stock de los componentes.**

¿Por qué?

1. Producto exige tener stock y calcular `disponible`.  
2. En el dominio real, un combo es un producto prearmado:  
   - si el local arma 10 combos por día → stock = 10  
   - aunque haya 100 aguas y 50 jamones.
3. Derivar stock del combo desde los componentes rompe la agregación.

PDF:

> “Decidí si un combo tiene stock propio o si su disponibilidad se deriva de la de sus componentes.”


## ✔ unidad_venta: UnidadMedida | None  
Hereda la asociación 0..1 de Producto.  
Un combo puede tener unidad (“u”) o ninguna unidad.



## ✔ categoria_principal: Categoria  
El combo aparece en el menú bajo una categoría (“Combos”, “Promociones”, etc.).  
Producto crea internamente el vínculo principal.


## ✔ habilitado: bool  
Hereda la lógica de disponibilidad de Producto:

```
disponible = habilitado and stock_cantidad > 0
```


## 🧩 3. Regla de cálculo del precio final

Regla exacta del PDF:

```
precio_final(cantidad) =
    (suma de componente.precio_final(1))
    × (1 - descuento)
    × cantidad
```

### ✔ No usa precio_base del combo  
### ✔ No redondea (solo ProductoPorPeso redondea)  
### ✔ Respeta polimorfismo  
### ✔ Funciona con combos anidados


## 🧩 4. Validaciones obligatorias

- Mínimo **2 componentes**.  
- Todos los componentes deben ser instancias de `Producto`.  
- Descuento en **[0, 1)**.  
- Cantidad entero y **>= 1**.  
- precio_base >= 0 (dato de catálogo).  
- Stock >= 0.


## 🧩 5. Relación estructural: Agregación

- Los componentes **no se crean** dentro del combo.  
- Los componentes **sobreviven** si el combo se elimina.  
- El combo **no es dueño** del ciclo de vida de los componentes.  
- `componentes()` devuelve una **tupla**, no la lista interna.

Esto cumple el PDF

## RESPUESTA PARA EL VIDEO

## 🧩 Agregación — ProductoCombo y sus componentes  

## ✔ ¿Qué miro en mi propio código para saber que implementé AGREGACIÓN?

La **línea exacta** que delata la agregación es:

```python
self._componentes: list[Producto] = componentes
```

## ✔ ¿Por qué esta línea demuestra agregación?

- Los componentes **se reciben ya construidos**.  
- El combo **solo guarda referencias** a objetos externos.  
- El combo **no crea** los componentes.  
- El combo **no controla** el ciclo de vida de los componentes.  
- Los componentes **existen antes y después** del combo.

Esto cumple exactamente lo que pide el PDF:

“Se reciben ya construidos y existen antes y después del combo.”


## ✔ ¿Qué le pasa a la parte cuando el todo deja de existir?

En **agregación**, la parte **sobrevive** al todo.

Ejemplo conceptual:

```
agua = ProductoSimple(...)
jamon = ProductoPorPeso(...)

combo = ProductoCombo(componentes=[agua, jamon], ...)
del combo
```

Después de `del combo`:

- `agua` sigue existiendo  
- `jamon` sigue existiendo  
- sus precios siguen intactos  
- su stock sigue intacto  
- su categoría sigue intacta  

El combo **no destruye ni modifica** a sus componentes.


## ✔ Frase perfecta para tu defensa oral

“En mi código, la agregación se ve en la línea `self._componentes = componentes`.  
Eso demuestra que el combo recibe productos ya construidos y solo guarda referencias.  
Los componentes existen antes y después del combo, y si el combo desaparece, los componentes siguen existiendo.  
El combo no controla el ciclo de vida de los componentes, por eso es agregación y no composición.”


### Nota

```
“Este modelo no busca representar un sistema real de stock o ventas.
Busca demostrar relaciones estructurales del dominio: composición, agregación y asociación.
En un sistema real, muchas de estas relaciones serían bidireccionales o incluso modeladas de otra forma,
pero en este parcial el objetivo es demostrar diseño orientado a objetos, no construir un sistema de producción.”
```

---
# 🧩 Producto destacado

ProductoDestacado **se mantiene como subclase de Producto** porque cumple plenamente el criterio **«es‑un»** dentro del dominio.

Un ProductoDestacado:

- tiene nombre → como cualquier Producto  
- tiene precio_base → como cualquier Producto  
- tiene stock_cantidad → como cualquier Producto  
- tiene unidad_venta → como cualquier Producto  
- tiene categoría principal → como cualquier Producto  
- tiene habilitado/disponible → como cualquier Producto  
- se exporta en el catálogo → como cualquier Producto  

La única diferencia es que agrega **orden_vidriera**, un atributo que afecta **solo la presentación** del catálogo, sin modificar comportamiento funcional.

Por lo tanto:

### ✔ ProductoDestacado **es‑un Producto**  
### ✔ La herencia es pertinente y se conserva  
### ✔ La especialización es semántica (presentación), no funcional  

## 🧠 Frase para la defensa oral

“ProductoDestacado cumple el criterio es‑un Producto.  
Comparte todo el comportamiento de Producto y solo agrega un atributo de presentación llamado orden_vidriera.  
No altera precio, stock, disponibilidad ni categorías, por lo que la herencia es pertinente y se mantiene como una especialización semántica del dominio.”

## ⭐ ProductoDestacado — Resumen de las dos decisiones faltantes del Requerimiento 3

## ✔ 1) Regla de `precio_final(cantidad)` en un ProductoDestacado
ProductoDestacado **no redefine** `precio_final`.  
Su especialización es **solo de presentación**, por lo que:

- mantiene exactamente la misma regla de precio que la subclase concreta de Producto de la que proviene.
- si es simple → usa la regla de ProductoSimple  
- si es por peso → usa la regla de ProductoPorPeso  
- si es combo → usa la regla de ProductoCombo  

**Justificación:**  
ProductoDestacado agrega únicamente `orden_vidriera`, que no afecta precio, stock ni disponibilidad.  
Por eso **no introduce comportamiento nuevo**, solo presentación.


## ✔ 2) ¿Cómo se destaca un ProductoPorPeso o un ProductoCombo?
ProductoDestacado **no reemplaza** a las otras subclases.  
Es un **rol opcional** del dominio que se aplica a cualquier Producto.

Para destacar un producto:

- se instancia un ProductoDestacado con los mismos datos del producto original  
- se agrega `orden_vidriera`  
- el cálculo de precio y el comportamiento funcional siguen siendo los de la clase concreta original

## Justificación:

La herencia se mantiene porque ProductoDestacado **es‑un Producto**, y su especialización es semántica (presentación), no funcional.

**Justificación integrada en el código (lo que exige HU‑P1‑05)**
1) La herencia se mantiene
class ProductoDestacado(Producto)  
Cumple el criterio es‑un.

1) Regla de precio_final explícita
ProductoDestacado no altera la regla:
return self._precio_base * cantidad  
Es la misma que ProductoSimple y ProductoPorPeso.
Coherente con “solo presentación”.

1) Cómo se destaca un producto por peso o un combo
Se instancia ProductoDestacado con los mismos datos del producto original.
El cálculo de precio sigue siendo el de la clase concreta.

1) orden_vidriera vive en ProductoDestacado
self._orden_vidriera = orden_vidriera

1) No se fuerza el modelo del catálogo
ProductoDestacado no toca stock, categorías, combos, ni disponibilidad.

1) UML, código y defensa coinciden
La herencia se mantiene.
El atributo está en la subclase.
La regla de precio está explícita.
El rol es opcional.

## 🧠 Frase para la defensa oral

“ProductoDestacado no redefine precio_final porque su especialización es solo de presentación.  
Para destacar un ProductoSimple, un ProductoPorPeso o un ProductoCombo, simplemente instancio ProductoDestacado con los mismos datos y agrego orden_vidriera.  
El comportamiento funcional sigue siendo el de la subclase concreta de Producto.”

“ProductoDestacado no diferencia si el producto era por unidad o por peso.
Usa la misma fórmula precio_base × cantidad.
La diferencia está en qué representa cantidad según el producto original: unidades para ProductoSimple, kilos/litros para ProductoPorPeso.
Así se cumple el polimorfismo sin if/elif ni isinstance().”

---


# 📦 Requerimiento 4 — Exportación con Protocol  
### Integración con librería externa y polimorfismo estructural

Este módulo implementa un mecanismo de exportación común para **productos del catálogo** y **fichas externas del punto de venta**, cumpliendo el requerimiento de usar **Protocol** en lugar de herencia clásica.

---

## 🧩 1. Contrato Exportable (Protocol)

Se define un contrato llamado **Exportable**, que exige únicamente el método:

`exportar(self) -> str`

Este contrato **no se hereda**.  
Las clases lo cumplen **por tener el método**, siguiendo el principio de **conformidad estructural** (duck typing).

Esto permite integrar objetos de terceros sin modificar su código.


## 🔌 2. Integración con la librería externa

La librería externa provee la clase:

`FichaPuntoDeVenta`

Esta clase ya implementa `exportar()`, por lo que **automáticamente cumple el contrato Exportable**, sin heredar nada y sin requerir adaptadores.

Esto demuestra que el diseño es flexible y desacoplado.


## 🔄 3. Implementación de exportar() en los productos

Cada clase concreta del catálogo implementa su propia versión de `exportar()`:

- ProductoSimple  
- ProductoPorPeso  
- ProductoCombo  
- ProductoDestacado  

El formato de la cadena es **de diseño libre**, ya que el parcial evalúa únicamente:

- que devuelva `str`  
- que cumpla el contrato  
- que funcione junto con la clase externa  


## 📤 4. Función exportar_catalogo(items)

Se implementa:

`exportar_catalogo(items: list[Exportable]) -> list[str]`

Esta función recibe **productos y fichas externas mezclados** en la misma lista y exporta todos los elementos mediante polimorfismo estructural:

- sin `isinstance()`  
- sin `if/elif`  
- sin herencia forzada  
- sin modificar la librería externa  

Solo llama:

`item.exportar()`


## 🧪 5. Pruebas realizadas

Se verificó:

- Exportación individual de cada tipo de producto  
- Exportación de la clase externa FichaPuntoDeVenta  
- Exportación de listas mixtas (productos + fichas)  
- Exportación de combos anidados  
- Polimorfismo estructural funcionando en runtime  

Todas las pruebas pasaron correctamente.


## 🎯 Cierre (versión corta)

El sistema de exportación quedó simple y flexible: definí un Protocol y cualquier objeto que tenga `exportar()` entra sin pedir permiso. Los productos y la ficha externa trabajan juntos sin herencia, sin instanceof y sin tocar código de terceros. Con eso, el requerimiento queda completamente cumplido y el diseño queda limpio, desacoplado y fácil de extender.


---


# 🧩 Decisiones globales del modelo

✔ Producto es abstracto  
No se instancian productos genéricos.  
Solo se instancian productos concretos:
- ProductoSimple
- ProductoPorPeso
- (más adelante) ProductoCombo
- (a analizar) ProductoDestacado

✔ Las validaciones van en el constructor de cada subclase  
Porque son reglas del tipo de producto, no del cálculo.

✔ precio_final siempre recibe cantidad  
El UML exige que todas las subclases respeten ese nombre de parámetro.

✔ precio_publicado formatea con :.2f  
Por eso las otras subclases no necesitan redondear.

---


