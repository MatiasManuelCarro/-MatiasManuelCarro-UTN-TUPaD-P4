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

# ⭐ ProductoDestacado — Decisiones de diseño y justificación (Requerimiento 3)

`ProductoDestacado` es una subclase concreta de `Producto` cuyo propósito es **alterar el orden de aparición en la vidriera del catálogo**.  
No modifica el precio, no modifica el stock, no modifica la categoría, no modifica la disponibilidad.  
Solo agrega **un atributo adicional** que afecta la presentación del catálogo.


## 🧩 1. ¿Por qué existe ProductoDestacado?

El UML lo marca con:

class ProductoDestacado {
    <<a revisar en el Requerimiento 3>>
    #_orden_vidriera int
}

Esto significa que el UML deja **abierta** la interpretación y vos debés justificarla.  
La decisión correcta es:

**ProductoDestacado existe para representar productos que deben aparecer primero en la vidriera del catálogo.**

Es una **especialización semántica**, no funcional.


## 🧩 2. ¿Qué agrega al dominio?

Agrega **un solo atributo**:

#_orden_vidriera int

Este atributo:

- no afecta el precio  
- no afecta el stock  
- no afecta la disponibilidad  
- no afecta la categoría  
- no afecta la lógica de venta  
- no afecta la lógica de combos  

Solo afecta **cómo se ordena el catálogo al exportarlo**.


## 🧩 3. ¿Por qué es una subclase y no un atributo en Producto?

Justificación fuerte:

- Porque no todos los productos necesitan orden especial.  
- Porque el UML explícitamente define una subclase.  
- Porque el orden de vidriera es una característica opcional del dominio.  
- Porque evita contaminar la clase base con atributos que no aplican a todos.  
- Porque respeta el principio de “especialización por comportamiento o presentación”.


## 🧩 4. ¿Qué representa orden_vidriera?

Es un entero que indica la prioridad de aparición en la vidriera.

Reglas:

- valores más bajos → aparecen primero  
- valores más altos → aparecen después  
- si dos productos tienen el mismo orden → se respeta el orden natural del catálogo  
- si no se define orden → el producto se comporta como uno normal


## 🧩 5. ¿Qué pasa si el producto destacado se elimina?

- Nada especial.  
- No afecta a otros productos.  
- No altera el catálogo.  
- No rompe invariantes.

ProductoDestacado **no controla** nada más que su propio orden.


## 🧩 6. ¿Qué NO hace ProductoDestacado?

Esto es clave para evitar errores:

- No cambia el precio  
- No aplica descuentos  
- No modifica stock  
- No altera categorías  
- No altera disponibilidad  
- No altera la lógica de combos  
- No altera la lógica de ProductoSimple o ProductoPorPeso  
- No altera la lógica de ProductoCombo  

Es **solo una marca de presentación**.


## 🧩 7. ¿Cómo se implementa?

Idea de constructor en Python (a nivel conceptual):

```python
class ProductoDestacado(Producto):
    def __init__(
        self,
        nombre: str,
        precio_base: float,
        stock_cantidad: float,
        unidad_venta: UnidadMedida | None,
        categoria_principal: Categoria,
        orden_vidriera: int,
        habilitado: bool = True,
    ) -> None:
        super().__init__(nombre, precio_base, stock_cantidad, unidad_venta, categoria_principal, habilitado)
        self._orden_vidriera = orden_vidriera
```


## 🧩 8. ¿Qué línea del código demuestra que es una especialización?

La línea exacta:

class ProductoDestacado(Producto):

Justificación:

- hereda todo el comportamiento de Producto  
- agrega solo el atributo de orden  
- no redefine precio_final  
- no redefine disponibilidad  
- no redefine stock  
- no redefine categorías  

Esto demuestra que es una **especialización semántica**, no funcional.


## 🧩 9. ¿Qué pasa con orden_vidriera cuando el producto desaparece?

- Nada.  
- El atributo muere con el objeto.  
- No afecta a otros productos.  
- No deja “huecos” en la vidriera.  
- No requiere reordenamiento global.



## 🧩 10. Frase perfecta para tu defensa oral

```
“ProductoDestacado es una especialización de Producto que agrega un atributo de presentación llamado orden_vidriera.  
No modifica la lógica de precio, stock, disponibilidad ni categorías.  
Solo altera el orden en que el catálogo se exporta.  
Es una subclase porque no todos los productos necesitan esta característica,
 y el UML lo define como una especialización opcional del dominio.”
```

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


