# ✅ Checklist exhaustiva de requisitos — Food Store (Programación IV)

> Podés ir marcando cada ítem con `[x]` cuando lo tengas implementado.

---

## 🧩 Dominio general y proyecto

- [ ] **Proyecto y estructura:**
  - [ ] `catalogo.py` contiene todo el dominio (Req. 1 a 4).
  - [ ] `libreria_externa.py` se incluye sin modificar.
  - [ ] `main.py` es el demo ejecutable.
  - [ ] `uml/modelo_final.md` contiene el diagrama final (Mermaid o PNG referenciado).
  - [ ] `README.md` explica qué hace el proyecto y cómo se ejecuta.
  - [ ] Type hints en todas las firmas públicas (PEP 8).
  - [ ] El proyecto corre con `python main.py` en Python 3.12 sin dependencias externas.

---

## 🧩 DomainError (excepción de dominio)

- [ ] **Definición:**
  - [ ] Existe una clase de excepción propia `DomainError`.
  - [ ] `DomainError` hereda de `ValueError`.
- [ ] **Uso:**
  - [ ] Se usa para todas las validaciones de dominio (nombre vacío, precio inválido, stock inválido, cantidad inválida, etc.).
  - [ ] Clasificar dos veces en la misma categoría lanza `DomainError`.
  - [ ] Menos de 2 componentes en `ProductoCombo` lanza `DomainError`.
  - [ ] Cantidad inválida en `precio_final` lanza `DomainError` según reglas de cada subclase.

---

## 🧩 UnidadMedida

- [ ] **Definición:**
  - [ ] `UnidadMedida` está definida como `@dataclass(frozen=True)`.
  - [ ] Tiene atributos: `nombre`, `simbolo`, `tipo`.
- [ ] **Reglas:**
  - [ ] Es inmutable: intentar reasignar `simbolo` lanza `FrozenInstanceError`.
  - [ ] `tipo` es solo dato descriptivo (`"masa"`, `"volumen"`, `"unidad"`), no se usa en reglas del parcial.

---

## 🧩 Categoria

- [ ] **Construcción:**
  - [ ] Constructor recibe `nombre` y opcionalmente `descripcion` (por defecto cadena vacía).
  - [ ] Valida que `nombre` no esté vacío ni sean solo espacios.
  - [ ] Si `nombre` está vacío, lanza `DomainError`.
- [ ] **Encapsulamiento:**
  - [ ] Atributos internos con guion bajo simple (`_nombre`, `_descripcion`).
  - [ ] Properties de solo lectura: `nombre`, `descripcion`.
  - [ ] No tiene setters: una vez creada, la categoría no cambia.

---

## 🧩 ProductoCategoria (vínculo de clasificación)

- [ ] **Relación estructural (composición):**
  - [ ] Representa el vínculo entre `Producto` y `Categoria`.
  - [ ] Tiene atributos internos: `_categoria`, `_es_principal` (y `_producto` como dueño).
- [ ] **Construcción:**
  - [ ] El vínculo se construye **solo dentro de Producto** (composición).
  - [ ] El código cliente nunca instancia `ProductoCategoria` directamente.
- [ ] **Encapsulamiento:**
  - [ ] Properties de solo lectura: `categoria`, `es_principal`.
  - [ ] No expone setters para `_es_principal`.
- [ ] **Invariante de clasificación:**
  - [ ] Siempre hay exactamente **una** clasificación principal (ni cero ni dos).
  - [ ] `clasificar_en(..., es_principal=True)` desmarca la anterior principal.
  - [ ] Clasificar dos veces en la misma categoría lanza `DomainError`.
- [ ] **Método protegido (opcional):**
  - [ ] Existe lógica para cambiar principal:
    - [ ] O un método protegido `#marcar_principal(valor bool)` invocado solo por el dueño.
    - [ ] O reemplazo del vínculo por uno nuevo (si se modeló inmutable).
  - [ ] La decisión se explica en el video.

---

## 🧩 Producto (clase abstracta, contrato del catálogo)

- [ ] **Definición:**
  - [ ] `Producto` es una clase abstracta (`ABC`).
  - [ ] Declara `@abstractmethod precio_final(cantidad: float) -> float`.
  - [ ] Ninguna instancia directa de `Producto` se usa en el dominio.
- [ ] **Atributos internos:**
  - [ ] `_nombre: str`
  - [ ] `_precio_base: float`
  - [ ] `_stock_cantidad: float`
  - [ ] `_habilitado: bool`
  - [ ] `_unidad_venta: UnidadMedida | None`
  - [ ] `_clasificaciones: list[ProductoCategoria]`
- [ ] **Validaciones de dominio (Req. 1):**
  - [ ] En el constructor de `Producto` se valida:
    - [ ] `nombre` no vacío.
    - [ ] `precio_base >= 0`.
    - [ ] `stock_cantidad >= 0`.
  - [ ] Si no se cumplen, se lanza `DomainError`.
- [ ] **Relación con Categoria (composición):**
  - [ ] El constructor recibe `categoria_principal`.
  - [ ] Crea internamente el primer `ProductoCategoria` con `es_principal=True`.
- [ ] **Relación con UnidadMedida (asociación 0..1):**
  - [ ] `unidad_venta` puede ser `None` (producto sin unidad es válido).
- [ ] **Properties públicas:**
  - [ ] `nombre` (solo lectura).
  - [ ] `precio_base` (solo lectura).
  - [ ] `unidad_venta` (solo lectura, puede ser `None`).
  - [ ] `disponible`:
    - [ ] Devuelve `True` solo si `_habilitado` es `True` y `_stock_cantidad > 0`.
  - [ ] `precio_publicado`:
    - [ ] Devuelve `"$ 12.50 / kg"` cuando hay unidad de venta (usa `simbolo`).
    - [ ] Devuelve `"$ 3.00"` cuando `unidad_venta` es `None`.
  - [ ] `categorias`:
    - [ ] Devuelve una **tupla** construida desde la lista interna.
    - [ ] No devuelve la lista interna.
  - [ ] `categoria_principal`:
    - [ ] Devuelve la `Categoria` principal (no el vínculo).
    - [ ] Si no hay principal, lanza `RuntimeError` (o equivalente coherente).
- [ ] **Métodos de dominio:**
  - [ ] `habilitar()` cambia `_habilitado` a `True`.
  - [ ] `deshabilitar()` cambia `_habilitado` a `False`.
  - [ ] `clasificar_en(categoria, es_principal=False)`:
    - [ ] Crea internamente un nuevo `ProductoCategoria`.
    - [ ] No devuelve el vínculo.
    - [ ] Si `es_principal=True`, desmarca la anterior principal.
    - [ ] Mantiene el invariante de una sola principal.
    - [ ] Lanza `DomainError` si se clasifica dos veces en la misma categoría.
- [ ] **Exportable (Req. 4):**
  - [ ] `Producto` implementa `exportar() -> str`.
  - [ ] El formato de la cadena es de diseño libre, pero devuelve `str`.

---

## 🧩 ProductoSimple (subclase de Producto)

- [ ] **Herencia:**
  - [ ] `ProductoSimple` hereda de `Producto`.
- [ ] **Reglas de cálculo (Req. 3):**
  - [ ] Fórmula: `precio_final = precio_base × cantidad`.
  - [ ] `cantidad` debe ser de **valor entero y >= 1**:
    - [ ] 3 y 3.0 válidos.
    - [ ] 2.5 no válido.
  - [ ] Si `cantidad` no cumple, lanza `DomainError`.
- [ ] **Validación de precio_base (según PDF):**
  - [ ] `precio_base` debe ser entero y >= 1:
    - [ ] 3 y 3.0 válidos.
    - [ ] 2.5 no válido.
  - [ ] Si no cumple, lanza `DomainError`.
- [ ] **Implementación:**
  - [ ] Constructor valida `precio_base` según regla de ProductoSimple.
  - [ ] Llama a `super().__init__` con todos los parámetros del dominio.
  - [ ] `precio_final(cantidad)`:
    - [ ] Valida cantidad según regla.
    - [ ] Devuelve `self._precio_base * cantidad`.
    - [ ] No redondea.

---

## 🧩 ProductoPorPeso (subclase de Producto)

- [ ] **Herencia:**
  - [ ] `ProductoPorPeso` hereda de `Producto`.
- [ ] **Reglas de cálculo (Req. 3):**
  - [ ] Fórmula: `precio_final = precio_base × cantidad`.
  - [ ] Resultado **redondeado a 2 decimales**.
  - [ ] `cantidad > 0`, admite decimales (ej: 0.250).
  - [ ] Si `cantidad <= 0`, lanza `DomainError`.
- [ ] **Validación de precio_base:**
  - [ ] `precio_base > 0`.
  - [ ] Admite decimales (ej: 8500.50).
  - [ ] Si no cumple, lanza `DomainError`.
- [ ] **Implementación:**
  - [ ] Constructor valida `precio_base > 0`.
  - [ ] Llama a `super().__init__`.
  - [ ] `precio_final(cantidad)`:
    - [ ] Valida cantidad > 0.
    - [ ] Devuelve `round(self._precio_base * cantidad, 2)`.
    - [ ] Es la **única** subclase que redondea.

---

## 🧩 ProductoCombo (subclase de Producto)

- [ ] **Herencia:**
  - [ ] `ProductoCombo` hereda de `Producto`.
- [ ] **Relación estructural (agregación):**
  - [ ] Tiene `_componentes: list[Producto]`.
  - [ ] Los componentes se reciben ya construidos.
  - [ ] Los componentes existen antes y después del combo (sobreviven al combo).
- [ ] **Atributos propios:**
  - [ ] `_componentes: list[Producto]`.
  - [ ] `_descuento: float`.
- [ ] **Reglas de cálculo (Req. 3):**
  - [ ] Fórmula:
    - [ ] `precio_final(cantidad) = (suma de componente.precio_final(1)) × (1 - descuento) × cantidad`.
  - [ ] `cantidad` debe ser de valor entero y >= 1:
    - [ ] 3 y 3.0 válidos.
    - [ ] 2.5 no válido.
  - [ ] `descuento` en `[0, 1)`:
    - [ ] Si está fuera de rango, lanza `DomainError`.
  - [ ] Menos de 2 componentes lanza `DomainError`.
- [ ] **Validación de componentes:**
  - [ ] Todos los componentes son instancias de `Producto`.
  - [ ] Se valida que la lista tenga al menos 2 elementos.
- [ ] **Implementación:**
  - [ ] Constructor recibe componentes y descuento.
  - [ ] Valida cantidad de componentes y rango de descuento.
  - [ ] Llama a `super().__init__` para el estado común.
  - [ ] `componentes()`:
    - [ ] Devuelve una tupla construida desde la lista interna.
    - [ ] No devuelve la lista interna.
  - [ ] `precio_final(cantidad)`:
    - [ ] Valida cantidad entero y >= 1.
    - [ ] Suma `componente.precio_final(1)` para cada componente.
    - [ ] Aplica `(1 - descuento)`.
    - [ ] Multiplica por `cantidad`.
- [ ] **Decisión sobre precio_base y stock del combo (Req. 3):**
  - [ ] Se decide si `precio_base` del combo:
    - [ ] Se recibe como dato de catálogo, o
    - [ ] Se deriva de sus componentes.
  - [ ] Se decide si `stock_cantidad` del combo:
    - [ ] Es propio, o
    - [ ] Se deriva de la disponibilidad de sus componentes.
  - [ ] La decisión se implementa coherente con `precio_publicado` y `disponible`.
  - [ ] La decisión se explica en el video.

---

## 🧩 ProductoDestacado (decisión obligatoria)

- [ ] **Decisión sobre la herencia:**
  - [ ] Se analiza si `ProductoDestacado` **es-un** `Producto`.
  - [ ] Se decide:
    - [ ] Mantener la herencia, o
    - [ ] Rediseñar (por ejemplo, composición, atributo en Producto, etc.).
- [ ] **Si se mantiene como subclase de Producto:**
  - [ ] `ProductoDestacado` implementa `precio_final(cantidad)` con una regla explícita.
  - [ ] Se explica cómo se destaca un `ProductoSimple`, `ProductoPorPeso` o `ProductoCombo`.
  - [ ] Tiene atributo `_orden_vidriera: int`.
  - [ ] Se justifica con criterio “es-un” del dominio.
- [ ] **Si se rediseña:**
  - [ ] Se define dónde vive `_orden_vidriera` (en Producto, en otra clase, etc.).
  - [ ] Se define qué productos pueden destacarse (todos, algunos).
  - [ ] La decisión queda implementada en el código (no solo en el video).
  - [ ] Se muestra la clase/atributo/relación que materializa la decisión.

---

## 🧩 Exportable (Protocol) y FichaPuntoDeVenta

- [ ] **Exportable (Req. 4):**
  - [ ] Se define `Exportable` como `Protocol` con `exportar() -> str`.
  - [ ] Ninguna clase del dominio hereda de `Exportable`.
  - [ ] La conformidad es estructural: las clases cumplen por tener el método.
- [ ] **FichaPuntoDeVenta (librería externa):**
  - [ ] `FichaPuntoDeVenta` ya tiene `exportar() -> str`.
  - [ ] No se modifica `libreria_externa.py` en ninguna línea.
- [ ] **exportar_catalogo:**
  - [ ] Se implementa `exportar_catalogo(items: list[Exportable]) -> list[str]`.
  - [ ] Acepta en la misma lista:
    - [ ] Productos del dominio.
    - [ ] Objetos `FichaPuntoDeVenta`.
  - [ ] Funciona en runtime con ambos tipos.
  - [ ] No usa `isinstance` ni herencia de `Exportable`.
  - [ ] La firma está declarada como `list[Exportable] -> list[str]`.

---

## 🧩 Demo ejecutable — main.py (Req. 5)

- [ ] **Catálogo mínimo:**
  - [ ] Crea al menos 4 productos (sin contar componentes de combos).
  - [ ] Usa las tres subclases de venta:
    - [ ] `ProductoSimple`.
    - [ ] `ProductoPorPeso`.
    - [ ] `ProductoCombo`.
- [ ] **Clasificaciones y unidades:**
  - [ ] Clasifica productos en categorías.
  - [ ] Asigna unidades de venta distintas (kg, unidad, etc.).
- [ ] **Cálculo de precios:**
  - [ ] Calcula `precio_final` con cantidades distintas para cada tipo.
- [ ] **Exportación:**
  - [ ] Crea al menos una `FichaPuntoDeVenta`.
  - [ ] Exporta productos y fichas juntos con `exportar_catalogo`.
  - [ ] Muestra el catálogo por consola.
- [ ] **Demostraciones clave:**
  - [ ] Composición:
    - [ ] `ProductoCategoria` solo nace dentro de `Producto`.
    - [ ] El cliente no construye ni reemplaza vínculos.
  - [ ] Agregación:
    - [ ] Los componentes sobreviven al combo y pueden reutilizarse en otros combos.
  - [ ] Falla temprana:
    - [ ] Instanciar `Producto` abstracto o subclase sin `precio_final` revienta al construir (TypeError).

---

## 🧩 Video de defensa (Req. 6.3)

- [ ] **Video:**
  - [ ] Duración entre 10 y 15 minutos.
  - [ ] Cámara encendida.
  - [ ] Audio claro.
  - [ ] Pantalla compartida mostrando ejecución y código.
- [ ] **Contenido:**
  - [ ] Responde las 4 preguntas sobre:
    - [ ] Composición, agregación, asociación (líneas exactas y ciclo de vida).
    - [ ] Decisión sobre `ProductoDestacado`.
    - [ ] ABC vs Protocol para `Exportable`.
    - [ ] Qué parte se implementó tal cual el diagrama y qué parte fue decisión propia.
  - [ ] Las decisiones defendidas se ven reflejadas en el código.

