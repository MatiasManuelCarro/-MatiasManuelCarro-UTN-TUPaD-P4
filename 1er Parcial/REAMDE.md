# Food Store - Catálogo de Productos

**Primera Evaluación Parcial - Programación IV**
**Autor:** Matias Manuel Carro
**UTN TUPaD** 

## Descripción del Proyecto
Este proyecto implementa el modelo de dominio para el catálogo de productos de Food Store, resolviendo el diseño orientado a objetos íntegramente en memoria sin bases de datos ni interfaces gráficas. El foco principal está puesto en la correcta aplicación de:
*   Encapsulamiento y validación de reglas de negocio.
*   Distinción estricta entre relaciones de Composición, Agregación y Asociación.
*   Análisis del criterio "es-un" para el uso justificado de la herencia.
*   Uso de contratos mediante tipado estructural (`Protocol`).

## Estructura de Archivos
*   `catalogo.py`: Contiene todo el modelo de dominio (clases, excepciones y lógica de negocio)
*   `libreria_externa.py`: Simula el sistema de caja provisto por un tercero; se integra al catálogo sin ser modificada en absoluto.
*   `main.py`: Demo ejecutable que instancia los objetos y demuestra el funcionamiento del sistema.

## Ejecución
El proyecto está desarrollado para ejecutarse en **Python 3.12** y no requiere dependencias externas.
Para correr la demostración completa del Requerimiento 5, ejecutar en la terminal:

    python main.py

## Decisiones de Diseño Principales

1. **Rediseño de ProductoDestacado:**
   En el modelo inicial, se proponía como una subclase de `Producto`. Al aplicar el criterio "es-un", se determinó que destacar un producto no lo convierte en un nuevo tipo base, ya que esto impediría destacar combos o productos por peso. Se rediseñó utilizando **composición**, donde `ProductoDestacado` envuelve a cualquier instancia de `Producto` existente.

2. **Derivación de estado en ProductoCombo:**
   El `precio_base` y la disponibilidad (`disponible`) de un combo no se reciben como datos estáticos en su construcción. Para mantener la coherencia del dominio, estas properties se derivan dinámicamente iterando sobre los componentes que el combo agrega.

3. **Contrato Exportable (Conformidad Estructural):**
   Para unificar la exportación de nuestros productos con la clase `FichaPuntoDeVenta` (la cual no podemos modificar), se utilizó un `Protocol` en lugar de una clase Abstracta (`ABC`). Esto permite aplicar Duck Typing, logrando que el catálogo exporte todo mediante el método `exportar()` sin forzar herencias artificiales.