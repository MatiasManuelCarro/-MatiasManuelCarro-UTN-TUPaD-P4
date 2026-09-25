# Food Store - Catálogo de Productos

**Primer Parcial - Programación 4**
**Autor:** Matias Manuel Carro
**UTN TUPaD** 

## Descripción del Proyecto
Este proyecto implementa el modelo de dominio para el catálogo de productos de Food Store, resolviendo el diseño orientado a objetos íntegramente en memoria sin bases de datos ni interfaces gráficas. El foco principal está puesto en la correcta aplicación de:
*   Encapsulamiento y validación de reglas de negocio.
*   Distinción estricta entre relaciones de Composición, Agregación y Asociación.
*   Análisis del criterio "es-un" para el uso justificado de la herencia.
*   Uso de contratos mediante tipado estructural (`Protocol`).

## Estructura de Archivos

```
Carro_Matias_P1_POO/
├── README.md 
├── catalogo.py 
├── libreria_externa.py 
├── main.py # 
├── link_video.txt # 
└── uml/
   └── modelo_final.md
```

*   `catalogo.py`: Contiene todo el modelo de dominio (clases, excepciones y lógica de negocio)
*   `libreria_externa.py`: Simula el sistema de caja provisto por un tercero; se integra al catálogo sin ser modificada en absoluto.
*   `main.py`: Demo ejecutable que instancia los objetos y demuestra el funcionamiento del sistema.

## Que contiene catalogo.py

###  `producto`
Superclase abstracta `Producto`. Define:
- Validaciones generales (nombre, precio_base, stock).
- Atributos internos comunes.
- Composición con `ProductoCategoria`.
- Properties públicas de solo lectura.
- Métodos abstractos `precio_final` y `exportar`.

Es el **núcleo del modelo**: todas las subclases se construyen a partir de él.

### `producto_simple`
Implementa `ProductoSimple`, un producto **unitario**:
- `precio_base` entero y ≥ 1.
- `cantidad` entera y ≥ 1.
- `precio_final` = precio_base × cantidad.
- Exporta: `PROD|nombre|precio_base`.


### `producto_por_peso`
Implementa `ProductoPorPeso`, un producto **decimal**:
- `precio_base` > 0 y admite decimales.
- `cantidad` > 0.
- `precio_final` redondea a 2 decimales.
- Exporta: `PROD_PESO|nombre|precio_base|unidad`.


### `producto_combo`
Implementa `ProductoCombo`, un producto **compuesto por agregación**:
- Requiere ≥ 2 componentes.
- Los componentes deben ser instancias de `Producto`.
- El precio y disponibilidad se **derivan dinámicamente** de los componentes.
- Exporta: `COMBO|nombre|cantidad_componentes`.

**Decisión de diseño:**  
Los componentes existen antes y después del combo es **agregación**, no composición.


### `producto_categoria`
Implementa `ProductoCategoria`, el vínculo de **composición** entre:
- un `Producto`
- una `Categoria`

El producto crea y controla este vínculo.  
Incluye el flag `es_principal`.


### `categoria`
Representa una categoría del catálogo.  
Solo contiene el nombre y es usada por `ProductoCategoria`.


### `unidad_medida`
Representa unidades como:
- kg  
- g  
- L  
- ml  

Incluye nombre, símbolo y tipo.


### `producto_destacado`
Implementa `ProductoDestacado`, es un **decorador**:
- NO hereda de `Producto` (decisión del parcial).
- Envuelve un producto existente.
- Agrega `orden_vidriera`.
- Exporta: `DEST|nombre_producto|orden`.

---

## Ejecución
El proyecto está desarrollado para ejecutarse en **Python 3.12** y no requiere dependencias externas.
Para correr ejecutar en la terminal:

```bash
    python main.py
```

## Decisiones de Diseño Principales

1. **Rediseño de ProductoDestacado:**
   En el modelo inicial, se proponía como una subclase de `Producto`. pero al aplicar el criterio **“es‑un”** se descartó esa opción: un producto destacado **no tiene precio, stock, unidad de venta ni categoría propia**, y tampoco se vende por sí mismo. Destacar un producto no lo convierte en un nuevo tipo de producto; solo agrega **como aparece en la vidriera**.  
   Por eso `ProductoDestacado` se modela mediante **agregación**, envolviendo cualquier instancia existente de `Producto` y asignándole un `orden_vidriera` sin alterar su identidad ni su ciclo de vida.


2. **Derivación de estado en ProductoCombo:**
   El `precio_base` y la disponibilidad (`disponible`) de un combo no se reciben como datos estáticos en su construcción. Para mantener la coherencia del dominio, estas properties se derivan dinámicamente utilizando los componentes que el combo agrega.

3. **Contrato Exportable (Conformidad Estructural):**
   Para unificar la exportación de nuestros productos con la clase `FichaPuntoDeVenta` (la cual no podemos modificar), se utilizó un `Protocol` en lugar de una clase Abstracta (`ABC`). Esto permite aplicar Duck Typing, logrando que el catálogo exporte todo mediante el método `exportar()` sin forzar herencias.