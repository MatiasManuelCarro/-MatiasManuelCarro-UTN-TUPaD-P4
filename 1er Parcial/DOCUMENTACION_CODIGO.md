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
        if not nombre.strip():  # verifica si esta vacio o son solo espacios en blanco
            raise DomainError("El nombre de la categoría no puede estar vacío")
        self._nombre = nombre.strip()
        self._descripcion = descripcion

    # estos property evitan setters
    # Mantiene la inmutabilidad lógica de la categoría: una vez creada, su nombre y #descripción no cambian.
    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion

```

Motivo:
- El nombre no puede ser vacío → regla del dominio.
- Atributos privados + properties → inmutabilidad lógica.
- No tiene setters: una categoría no cambia una vez creada.


## ✔ Justificación de diseño
- **Inmutabilidad lógica**: una categoría es parte fija del catálogo; su nombre y descripción no cambian luego de creada.  
- **Sin setters**: evita inconsistencias y respeta el modelo del PDF (las categorías son entidades estáticas).  
- **Encapsulación**: los atributos internos (`_nombre`, `_descripcion`) quedan protegidos y solo se exponen mediante lectura.

## ✔ Qué hace cada property
- **`nombre`** → expone el nombre validado de la categoría.  
- **`descripcion`** → expone la descripción opcional.  
Ambos son **solo lectura**.


---

# 🧩 ProductoCategoria (Composición)


### ✔ Rol en el dominio
`ProductoCategoria` representa el **vínculo de composición** entre un `Producto` y una `Categoria`.  
El vínculo existe únicamente dentro del producto y es gestionado por él (no por el cliente).

```python
class ProductoCategoria:
    def __init__(
        self, producto: Producto, categoria: Categoria, es_principal: bool = False
    ) -> None:
        self._producto = (
            producto  # ! aca se crea la composicion Producto → ProductoCategoria
        )
        self._categoria = categoria
        self._es_principal = es_principal
```

### ✔ Atributos internos
- **`_producto`** → referencia al producto dueño del vínculo (composición).  
- **`_categoria`** → categoría asociada.  
- **`_es_principal`** → indica si esta categoría es la principal del producto.

```python
    @property
    def categoria(self) -> Categoria:
        return self._categoria

    @property
    def es_principal(self) -> bool:
        return self._es_principal
```

### ✔ Properties (solo lectura)
- **`categoria`** → expone la categoría asociada; el cliente puede consultarla pero no modificarla.  
- **`es_principal`** → indica si esta categoría es la principal; también es solo lectura.

```python
    def _marcar_principal(self, valor: bool) -> None:
        self._es_principal = valor
```

### ✔ Método interno
- **`_marcar_principal(valor)`** → usado exclusivamente por `Producto` para cambiar la categoría principal.  
  No está disponible para el cliente, preservando la integridad del vínculo.

### ✔ Justificación de diseño
- **Composición real**: el vínculo nace y muere con el producto.  
- **Inmutabilidad externa**: el cliente no puede alterar categorías ni marcar principal directamente.  
- **Encapsulación**: los atributos internos quedan protegidos; solo se exponen mediante lectura.  
- **Cumple el PDF**: la reclasificación se hace únicamente desde `Producto.clasificar_en()`.

### ✔ Línea que evidencia la composición

```python
self._producto = producto
```

---

# 🧩 Producto — Superclase abstracta del catálogo

### ✔ Rol en el dominio
`Producto` es la **superclase abstracta** que define el contrato común de todos los productos del catálogo.  
Incluye validaciones, atributos esenciales, clasificación en categorías y operaciones polimórficas como `precio_final` y `exportar`.

```python
class Producto(ABC):
    def __init__(..., categoria_principal: Categoria, ...) -> None:
        ...
        self._clasificaciones: list[ProductoCategoria] = []
        principal = ProductoCategoria(self, categoria_principal, es_principal=True)
        self._clasificaciones.append(principal)
```

### ✔ Atributos internos
- **`_nombre`** → nombre validado del producto.  
- **`_precio_base`** → precio base según el tipo de producto.  
- **`_stock_cantidad`** → cantidad disponible.  
- **`_habilitado`** → indica si el producto está activo.  
- **`_unidad_venta`** → unidad opcional (solo para productos por peso).  
- **`_clasificaciones`** → lista interna de `ProductoCategoria` (multiplicidad `*`).

### ✔ Properties públicos (solo lectura)

```python
@property  
def nombre(self) -> str: ...

@property  
def precio_base(self) -> float: ...

@property  
def unidad_venta(self) -> UnidadMedida | None: ...

@property  
def disponible(self) -> bool: ...

@property  
def precio_publicado(self) -> str: ...

@property  
def categorias(self) -> tuple[ProductoCategoria, ...]: ...

@property  
def categoria_principal(self) -> Categoria: ...
```

- **`nombre` / `precio_base` / `unidad_venta`** → exponen atributos esenciales.  
- **`disponible`** → habilitado y con stock mayor a cero.  
- **`precio_publicado`** → formato del precio para el catálogo.  
- **`categorias`** → **tupla inmutable** construida desde la lista interna (retorno protegido).  
- **`categoria_principal`** → devuelve la categoría marcada como principal.

### ✔ Métodos públicos

```python
def habilitar(self) -> None: ...  
def deshabilitar(self) -> None: ...  
def clasificar_en(self, categoria: Categoria, es_principal: bool = False) -> None: ...
```

- **`habilitar` / `deshabilitar`** → controlan disponibilidad lógica.  
- **`clasificar_en`** → agrega una clasificación, evita duplicados y permite cambiar la categoría principal.

### ✔ Métodos abstractos

```python
@abstractmethod  
def precio_final(self, cantidad: float) -> float: ...

@abstractmethod  
def exportar(self) -> str: ...
```

- **`precio_final`** → cálculo polimórfico según la subclase.  
- **`exportar`** → contrato de exportación; cada tipo define su formato.

### ✔ Justificación de diseño
- **Composición real**: el producto crea su propia categoría principal.  
- **Polimorfismo**: cada subclase implementa su propio `precio_final` y `exportar`.  
- **Encapsulación**: los atributos internos se exponen solo mediante lectura.  
- **Retorno protegido**: `categorias` devuelve una tupla, nunca la lista interna.  
- **Cumple el PDF**: sin ramificar por tipo, con ciclo de vida controlado y validaciones coherentes.

### ✔ Línea que evidencia la composición
```python
principal = ProductoCategoria(self, categoria_principal, es_principal=True)
```

---

# 🧩 ProductoSimple — Producto unitario con precio entero (se vende por unidad)

### ✔ Rol en el dominio
`ProductoSimple` representa productos **unitarios**, vendidos por cantidad entera (ej.: latas, cajas, botellas).  
Extiende `Producto` aplicando las reglas específicas del parcial: precio base entero y cantidad entera.

```python
class ProductoSimple(Producto):
    def __init__(..., precio_base: float, ...) -> None:
        # ProductoSimple: precio_base debe ser entero y >= 1
        if precio_base < 1 or precio_base != int(precio_base):
            raise DomainError("precio_base debe ser entero y no puede ser negativo en ProductoSimple")

        super().__init__(...)
```

### ✔ Validaciones específicas
```python
        # ProductoSimple: precio_base debe ser entero y >= 1
        if precio_base < 1 or precio_base != int(precio_base):
            raise DomainError(
                "precio_base debe ser entero y no puede ser negativo en ProductoSimple"
            )
```

- **`precio_base` entero y ≥ 1** → evita precios decimales en productos unitarios.  
- **Cantidad entera y ≥ 1** en `precio_final` → respeta la naturaleza del producto simple.

El constructor de `ProductoSimple` primero valida sus reglas específicas (precio_base entero y ≥ 1).  
Si la validación falla, la creación del objeto se aborta inmediatamente.  
Si la validación pasa, delega la construcción completa del producto al constructor de `Producto` mediante `super().__init__`, donde se inicializan los atributos internos y se crea la composición `ProductoCategoria`.


### ✔ Cálculo del precio final

```python
def precio_final(self, cantidad: float) -> float:
    if cantidad < 1 or cantidad != int(cantidad):
        raise DomainError("La cantidad debe ser entera y >= 1 en ProductoSimple")
    return self._precio_base * cantidad

- Multiplica el precio base por la cantidad.  
- No admite fracciones ni cantidades menores a 1.
```

### ✔ Exportación

```python
def exportar(self) -> str:
    return f"PROD|{self.nombre}|{self.precio_base}"
```

- Formato definido por el PDF para productos simples.  
- Cumple el contrato `exportar()` de `Producto` mediante polimorfismo estructural.

### ✔ Justificación de diseño
- **Especialización real**: aplica reglas propias de productos unitarios.  
- **Polimorfismo**: implementa su versión de `precio_final` y `exportar`.  
- **Validación temprana**: evita estados inválidos desde el constructor.  
- **Cumple el PDF**: sin ramificar por tipo, con reglas claras y encapsuladas en la subclase.

---

# ✔ Cómo funciona `super()` en el constructor

`ProductoSimple` no construye el objeto directamente.  
Primero ejecuta sus validaciones específicas (precio_base entero y ≥ 1).  
Si alguna falla, la creación del objeto se aborta inmediatamente.

Si las validaciones pasan, `ProductoSimple` llama a:

super().__init__(nombre, precio_base, stock_cantidad, unidad_venta, categoria_principal, habilitado)

Esto **no crea un objeto nuevo**, sino que:

- **le pasa los parámetros a `Producto`**,  
- **Producto ejecuta sus validaciones generales**,  
- **Producto asigna todos los atributos internos**,  
- **Producto crea la composición `ProductoCategoria`**,  
- **Producto deja el objeto completamente construido y consistente**.

Por lo tanto:

- `ProductoSimple` **solo valida reglas propias**.  
- `Producto` es quien **realmente construye el objeto**.  
- `super()` es la forma de delegar la construcción al constructor de la superclase.


---

# 🧩 ProductoPorPeso — Producto vendido por peso/volumen

### ✔ Rol en el dominio
`ProductoPorPeso` representa productos vendidos por **cantidad decimal** (kg, g, litros, ml).  
Extiende `Producto` aplicando las reglas específicas del parcial: precio base decimal y cálculo con redondeo.

```python
class ProductoPorPeso(Producto):
    def __init__(..., precio_base: float, ...) -> None:
        # ProductoPorPeso: precio_base > 0 y admite decimales
        if precio_base <= 0:
            raise DomainError("precio_base debe ser > 0 para ProductoPorPeso")

        super().__init__(...)
```

### ✔ Validaciones específicas
```python
        # ProductoPorPeso: precio_base > 0 y admite decimales
        if precio_base <= 0:
            raise DomainError("precio_base debe ser > 0 para ProductoPorPeso")
```

- **`precio_base > 0`** → evita precios nulos o negativos.  
- **Admite decimales** → a diferencia de `ProductoSimple`, no exige entero.  
- **Cantidad > 0** en `precio_final` → respeta la naturaleza del producto por peso.

### Llamada al super()

```python
        super().__init__(
            nombre,
            precio_base,
            stock_cantidad,
            unidad_venta,
            categoria_principal,
            habilitado,
        )
```
**Relación con `super()`**

`ProductoPorPeso` solo valida su regla específica (`precio_base > 0`).  
Si la validación pasa, delega la construcción completa del objeto al constructor de `Producto` mediante `super().__init__`, donde se inicializan atributos internos y se crea la composición `ProductoCategoria`.

### ✔ Cálculo del precio final

```python
def precio_final(self, cantidad: float) -> float:
    if cantidad <= 0:
        raise DomainError("La cantidad debe ser > 0 en ProductoPorPeso")
    return round(self._precio_base * cantidad, 2)
```

- Multiplica el precio base por la cantidad decimal.  
- **Redondea a 2 decimales** (única subclase que lo hace).  
- Permite cantidades como 0.250, 1.75, etc.

### ✔ Exportación

```python
def exportar(self) -> str:
    return f"PROD_PESO|{self.nombre}|{self.precio_base}|{self.unidad_venta.simbolo}"
```

- Formato definido por el PDF para productos por peso.  
- Incluye la unidad de venta (kg, g, L, ml).

### ✔ Justificación de diseño
- **Especialización real**: aplica reglas propias de productos por peso/volumen.  
- **Polimorfismo**: implementa su versión de `precio_final` y `exportar`.  
- **Validación temprana**: evita estados inválidos desde el constructor.  
- **Cumple el PDF**: admite decimales, valida cantidad > 0 y redondea a 2 decimales.




---


# 🧺 6. ProductoCombo — **Decisión de diseño clave del parcial**

# 🧩 ProductoCombo — Producto compuesto por agregación

### ✔ Rol en el dominio

`ProductoCombo` representa un **producto del catálogo** formado por otros productos ya existentes.  
A diferencia de `ProductoCategoria` (composición), acá la relación es **agregación**:  
los componentes **no nacen ni mueren** con el combo; simplemente **se agrupan**.

```python
class ProductoCombo(Producto):
    def __init__(..., componentes: list[Producto], descuento: float, ...) -> None:
        if len(componentes) < 2:
            raise DomainError("Un ProductoCombo debe tener al menos 2 componentes")

        for comp in componentes:
            if not isinstance(comp, Producto):
                raise DomainError("Todos los componentes de un combo deben ser Productos")

        if not (0 <= descuento < 1):
            raise DomainError("El descuento debe estar en el rango [0, 1)")

        super().__init__(nombre, precio_base=0.0, stock_cantidad=0.0, ...)

        self._componentes = componentes
        self._descuento = descuento
```

### ✔ Validaciones específicas
- **Mínimo 2 componentes** → un combo no puede ser unitario.  
- **Todos deben ser `Producto`** → admite cualquier subclase (`Simple`, `PorPeso`, otro `Combo`).  
- **Descuento en [0, 1)** → regla del PDF.

### ✔ Decisión de diseño: Agregación
Los componentes **se reciben ya construidos** y **existen antes y después del combo**.

Esto significa:

- El combo **no es dueño** del ciclo de vida de los componentes.  
- Si el combo se elimina, los productos **siguen existiendo**.  
- El combo **no modifica** el estado interno de los componentes.  
- Los componentes pueden estar en otros combos o venderse individualmente.

### ✔ Línea que evidencia la agregación

```python
self._componentes = componentes
```

Esta línea muestra que:

- El combo **no crea** los componentes.  
- Solo **guarda referencias** a objetos ya existentes.  
- No controla su destrucción ni su ciclo de vida.

### ✔ Properties (retorno protegido)

@property  
def componentes(self) -> tuple[Producto, ...]:
    return tuple(self._componentes)

- Devuelve una **tupla**, no la lista interna.  
- Protege la colección del combo.  
- Los objetos dentro **no se copian** (cada uno se protege con sus propias properties).

### ✔ Cálculo del precio final

```
def precio_final(self, cantidad: float) -> float:
    if cantidad < 1 or cantidad != int(cantidad):
        raise DomainError("La cantidad debe ser un entero >= 1 para ProductoCombo")

    subtotal = sum(p.precio_final(1) for p in self._componentes)
    total_con_descuento = subtotal * (1 - self._descuento)
    return total_con_descuento * cantidad

- Suma el precio final unitario de cada componente.  
- Aplica el descuento del combo.  
- Multiplica por la cantidad.  
- Respeta polimorfismo: cada componente calcula su propio precio.

### ✔ Exportación

def exportar(self) -> str:
    return f"COMBO|{self.nombre}|{len(self._componentes)}"

- Formato definido por el PDF.  
- Exporta nombre y cantidad de componentes.

### ✔ Justificación de diseño
- **Agregación real**: los componentes existen independientemente del combo.  
- **Polimorfismo**: cada componente aporta su precio final.  
- **Retorno protegido**: `componentes` devuelve una tupla.  
- **Validación temprana**: evita combos inválidos desde el constructor.  
- **Cumple el PDF**: descuento en [0,1), mínimo 2 componentes, sin setters, sin ramificar por tipo.

## 🎯 Cierre coloquial para explicar ProductoCombo (agregación)


En el combo no inventamos productos nuevos: simplemente **juntamos productos que ya existen** y los tratamos como un solo ítem del catálogo.  
Los componentes **no dependen del combo**, viven antes y después de él, y si cambian su precio o se quedan sin stock, el combo se actualiza solo.  
La línea que lo muestra clarito es cuando guardamos la lista que viene de afuera: `self._componentes = componentes`.  
Eso es agregación pura: el combo **usa** productos, pero **no los posee**.


---

# 🟨 Rediseño de `ProductoDestacado` — Justificación completa

## 🟦 Reemplazo de la herencia
El diseño original asumía que *ProductoDestacado es‑un Producto*, pero destacar un producto **no modifica** su precio_final, stock, unidad_venta, categorías ni comportamiento.  
Solo agrega **información de presentación** (orden en la vidriera).  
Por lo tanto, **no corresponde usar herencia**.

La herencia se reemplaza por **composición**:  
`ProductoDestacado` ahora **envuelve** a un `Producto` existente.

### Implementación

```python
class ProductoDestacado:
    def __init__(self, producto: Producto, orden_vidriera: int) -> None:
        self._producto = producto
        self._orden_vidriera = orden_vidriera

    @property
    def orden_vidriera(self) -> int:
        return self._orden_vidriera

    @property
    def producto(self) -> Producto:
        return self._producto

    def exportar(self) -> str:
        return f"DEST|{self._producto.nombre}|{self._orden_vidriera}"
```


## 🟩 Dónde vive `orden_vidriera`
`orden_vidriera` **no pertenece al producto**, sino a la **forma en que se muestra** en la vidriera.  
Por eso vive en el **envoltorio** `ProductoDestacado` y no en el producto original.

Esto respeta el principio de responsabilidad única:  
el producto mantiene su lógica de negocio, y el destacado maneja la presentación.



## 🟪 Qué productos pueden destacarse
Con la versión anterior (herencia), solo podían destacarse los productos que heredaban de `ProductoDestacado`.

Con la nueva versión (composición), pueden destacarse **todos los productos del catálogo**, porque el envoltorio recibe:

producto: Producto

Esto permite destacar:

- ProductoSimple  
- ProductoPorPeso  
- ProductoCombo  
- Cualquier otro tipo futuro  

Sin duplicar ni recrear productos.



## 🟫 Compatibilidad con el Protocol
`ProductoDestacado` sigue cumpliendo el Protocol `exportar()`:

DEST|{nombre_del_producto}|{orden_vidriera}

No necesita heredar de `Producto` ni de `Exportable`.  
Cumple por **conformidad estructural**, tal como exige el Requerimiento 4.



## 🟧 Resumen para defensa oral
Rediseñé `ProductoDestacado` porque no cumple el criterio es‑un Producto.  
No modifica precio_final, stock, unidad_venta ni categorías.  
Solo agrega un atributo de presentación llamado `orden_vidriera`.  
Por eso reemplazo la herencia por composición: `ProductoDestacado` envuelve a un `Producto` existente.  
Así cualquier producto del catálogo puede destacarse sin duplicarlo, y `orden_vidriera` vive en el envoltorio, no en el producto.  
El diseño queda más limpio, más flexible y más alineado con el dominio.

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

# UML

```mermaid
classDiagram
direction LR

%% ============================
%% Protocol
%% ============================
class Exportable {
    <<protocol>>
    +exportar() str
}

%% ============================
%% Clases del dominio
%% ============================
class Producto {
    <<abstract>>
    -nombre: str
    -precio_base: float
    -stock_cantidad: float
    -unidad_venta: UnidadMedida
    -categoria_principal: Categoria
    +precio_final(cantidad: float) float
    +exportar() str
}

class ProductoSimple {
    +precio_final(cantidad: float) float
    +exportar() str
}

class ProductoPorPeso {
    +precio_final(kg: float) float
    +exportar() str
}

class ProductoCombo {
    -componentes: list~Producto~
    -descuento: float
    +precio_final(cantidad: float) float
    +exportar() str
}

class ProductoDestacado {
    -orden_vidriera: int
    +precio_final(cantidad: float) float
    +exportar() str
}

class Categoria {
    -nombre: str
}

class UnidadMedida {
    -nombre: str
    -simbolo: str
    -tipo: str
}

%% ============================
%% Clase externa
%% ============================
class FichaPuntoDeVenta {
    -_codigo: str
    -_detalle: str
    +exportar() str
}

%% ============================
%% Relaciones
%% ============================

%% Herencia
Producto <|-- ProductoSimple
Producto <|-- ProductoPorPeso
Producto <|-- ProductoCombo
Producto <|-- ProductoDestacado

%% Composición (Combo contiene Productos)
ProductoCombo *-- Producto : componentes 1..*

%% Agregación (Producto tiene Categoria y UnidadMedida)
Producto o-- Categoria : 1
Producto o-- UnidadMedida : 0..1

%% Conformidad estructural con Protocol
ProductoSimple ..|> Exportable
ProductoPorPeso ..|> Exportable
ProductoCombo ..|> Exportable
ProductoDestacado ..|> Exportable
FichaPuntoDeVenta ..|> Exportable
```


---

# ✅ **2. UML en PlantUML (para exportar PNG)**

```markdown
```plantuml
@startuml
skinparam classAttributeIconSize 0

' ============================
' Protocol
' ============================
class Exportable <<protocol>> {
    +exportar(): String
}

' ============================
' Clases del dominio
' ============================
abstract class Producto {
    -nombre: String
    -precio_base: float
    -stock_cantidad: float
    -unidad_venta: UnidadMedida
    -categoria_principal: Categoria
    +precio_final(cantidad: float): float
    +exportar(): String
}

class ProductoSimple {
    +precio_final(cantidad: float): float
    +exportar(): String
}

class ProductoPorPeso {
    +precio_final(kg: float): float
    +exportar(): String
}

class ProductoCombo {
    -componentes: List<Producto>
    -descuento: float
    +precio_final(cantidad: float): float
    +exportar(): String
}

class ProductoDestacado {
    -orden_vidriera: int
    +precio_final(cantidad: float): float
    +exportar(): String
}

class Categoria {
    -nombre: String
}

class UnidadMedida {
    -nombre: String
    -simbolo: String
    -tipo: String
}

' ============================
' Clase externa
' ============================
class FichaPuntoDeVenta {
    -_codigo: String
    -_detalle: String
    +exportar(): String
}

' ============================
' Relaciones
' ============================

' Herencia
Producto <|-- ProductoSimple
Producto <|-- ProductoPorPeso
Producto <|-- ProductoCombo
Producto <|-- ProductoDestacado

' Composición
ProductoCombo *-- Producto : componentes 1..*

' Agregación
Producto o-- Categoria : 1
Producto o-- UnidadMedida : 0..1

' Conformidad estructural con Protocol
ProductoSimple ..|> Exportable
ProductoPorPeso ..|> Exportable
ProductoCombo ..|> Exportable
ProductoDestacado ..|> Exportable
FichaPuntoDeVenta ..|> Exportable

@enduml
```
```