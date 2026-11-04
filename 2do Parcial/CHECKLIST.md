### Fase 1: Configuración Inicial - Backend
- [ ] Crear entorno virtual (`.venv`).
- [ ] Instalar dependencia FastAPI.
- [ ] Instalar dependencia SQLModel.
- [ ] Instalar dependencia Pydantic v2.
- [ ] Instalar dependencias para PostgreSQL (ej. psycopg2/asyncpg).
- [ ] Crear archivo `requirements.txt`.
- [ ] Crear directorio `app/`.
- [ ] Crear archivo `app/__init__.py`.
- [ ] Crear archivo `app/main.py`.
- [ ] Habilitar `CORSMiddleware` en `main.py` para el origen del frontend.
- [ ] Crear directorio `app/core/`.
- [ ] Crear archivo `app/core/__init__.py`.
- [ ] Crear archivo `app/core/database.py`.
- [ ] Configurar cadena de conexión a PostgreSQL en `database.py`.
- [ ] Definir el `engine` de SQLModel en `database.py`.
- [ ] Definir la dependencia `get_session` (yield Session) en `database.py`.
- [ ] Crear archivo `app/core/seed.py`.
- [ ] Crear directorio `app/modules/`.
- [ ] Crear directorio `app/modules/unidades_medida/` con `__init__.py`, `model.py`, `router.py`.
- [ ] Crear directorio `app/modules/categorias/` con `__init__.py`, `router.py`, `model.py`, `schema.py`, `service.py`.
- [ ] Crear directorio `app/modules/productos/` con `__init__.py`, `router.py`, `model.py`, `schema.py`, `service.py`.
- [ ] Crear directorio `tests/`.

### Fase 2: Configuración Inicial - Frontend
- [ ] Crear proyecto React + TypeScript usando Vite.
- [ ] Configurar `tsconfig.json` con `strict: true`.
- [ ] Asegurar que no se utilicen tipos `any` en TypeScript.
- [ ] Instalar Tailwind CSS 4.
- [ ] Configurar estilos de Tailwind (enfoque utility-first).
- [ ] Eliminar librerías no permitidas (Axios, TanStack Query, Zustand, librerías de componentes).
- [ ] Crear directorio `src/components/`.
- [ ] Crear directorio `src/types/`.

### Fase 3: Modelado de Datos (SQLModel)
#### Entidad UnidadMedida (`model.py`)
- [ ] Declarar clase `UnidadMedida` como tabla (`table=True`).
- [ ] Definir campo `id` como entero y Primary Key.
- [ ] Definir campo `nombre` de tipo string y único.
- [ ] Definir campo `simbolo` de tipo string y único.
- [ ] Crear Enum para tipos de unidad (`peso`, `volumen`, `contable`).
- [ ] Definir campo `tipo` usando el Enum creado.
- [ ] Configurar `Relationship` hacia `Producto` (`back_populates`).

#### Entidad Categoria (`model.py`)
- [ ] Declarar clase `Categoria` como tabla (`table=True`).
- [ ] Definir campo `id` como entero y Primary Key.
- [ ] Definir campo `nombre` de tipo string (obligatorio).
- [ ] Definir campo `descripcion` de tipo string (opcional).
- [ ] Definir campo `activo` como booleano, `NOT NULL`, con default `true`.
- [ ] Definir campo `anulado_at` como TIMESTAMP (datetime), nullable.

#### Entidad ProductoCategoria - Tabla Intermedia (`model.py`)
- [ ] Declarar clase `ProductoCategoria` como tabla (`table=True`).
- [ ] Definir campo `producto_id` como FK a `Producto`, y parte de la PK compuesta.
- [ ] Definir campo `categoria_id` como FK a `Categoria`, y parte de la PK compuesta.
- [ ] Definir campo `es_principal` como booleano, `NOT NULL`, con default `false`.

#### Entidad Producto (`model.py`)
- [ ] Declarar clase `Producto` como tabla (`table=True`).
- [ ] Definir campo `id` como entero y Primary Key.
- [ ] Definir campo `unidad_venta_id` como entero, FK a `UnidadMedida`, `NOT NULL`.
- [ ] Definir campo `nombre` de tipo string (obligatorio).
- [ ] Definir campo `descripcion` de tipo string.
- [ ] Definir campo `precio_base` como numérico decimal.
- [ ] Definir campo `stock_cantidad` como numérico decimal, default `0`.
- [ ] Definir campo `disponible` como booleano, `NOT NULL`, default `true`.
- [ ] Definir campo `activo` como booleano, `NOT NULL`, default `true`.
- [ ] Definir campo `anulado_at` como TIMESTAMP (datetime), nullable.
- [ ] Configurar `Relationship` `unidad_venta` hacia `UnidadMedida` (`back_populates`).
- [ ] Configurar `Relationship` `categorias` hacia `Categoria` usando `link_model=ProductoCategoria`.

### Fase 4: Core y Catálogos Base
#### Seed Inicial (`app/core/seed.py`)
- [ ] Crear lógica para verificar si la tabla `UnidadMedida` está vacía.
- [ ] Crear script para insertar unidad `kilogramo` (`kg`, peso).
- [ ] Crear script para insertar unidad `gramo` (`g`, peso).
- [ ] Crear script para insertar unidad `litro` (`L`, volumen).
- [ ] Crear script para insertar unidad `mililitro` (`mL`, volumen).
- [ ] Crear script para insertar unidad `pieza` (`u`, contable).
- [ ] Crear script para insertar unidad `docena` (`doc`, contable).
- [ ] Ejecutar inserción en base de datos solo si estaba vacía.

#### Router Unidades de Medida
- [ ] Implementar endpoint `GET /api/v1/unidades-medida`.
- [ ] Asegurar que `GET /api/v1/unidades-medida` retorne 200 y el catálogo completo.

### Fase 5: Módulo Categorías (Schemas & Endpoints)
#### Schemas de Categoría (`schema.py`)
- [ ] Crear schema `CategoriaBase`.
- [ ] Definir validación Pydantic (`Field`): `nombre` con `min_length=3`.
- [ ] Definir campo `descripcion` opcional en Base/Create.
- [ ] Crear schema `CategoriaCreate` heredando de Base.
- [ ] Crear schema `CategoriaUpdate` heredando de Base.
- [ ] Crear schema `CategoriaPublic`.
- [ ] Incluir `id` en `CategoriaPublic`.
- [ ] Incluir `nombre` en `CategoriaPublic`.
- [ ] Incluir `descripcion` en `CategoriaPublic`.
- [ ] Incluir `activo` en `CategoriaPublic`.
- [ ] Incluir `anulado_at` en `CategoriaPublic`.

#### Servicios y Router Categorías (`service.py` y `router.py`)
- [ ] Inyectar dependencia de BD (Session) en endpoints.
- [ ] Configurar delegación de lógica desde `router.py` a `service.py`.
- [ ] Endpoint `POST /api/v1/categorias`: Validar `nombre` único entre activas (RN-02), lanzar `409` si falla.
- [ ] Endpoint `POST /api/v1/categorias`: Persistir nueva categoría y retornar 201.
- [ ] Endpoint `GET /api/v1/categorias`: Implementar listado.
- [ ] Endpoint `GET /api/v1/categorias`: Implementar filtro `activo`.
- [ ] Endpoint `GET /api/v1/categorias`: Implementar filtro `search` (coincidencia parcial de nombre).
- [ ] Endpoint `GET /api/v1/categorias/{id}`: Buscar por ID, lanzar `404` si no existe (RN-03).
- [ ] Endpoint `PUT /api/v1/categorias/{id}`: Lanzar `404` si ID no existe.
- [ ] Endpoint `PUT /api/v1/categorias/{id}`: Validar que no esté anulada, lanzar `409` si lo está (RN-05).
- [ ] Endpoint `PUT /api/v1/categorias/{id}`: Validar nombre único (RN-02).
- [ ] Endpoint `PUT /api/v1/categorias/{id}`: Actualizar `nombre` y `descripcion` y retornar 200.
- [ ] Endpoint `DELETE /api/v1/categorias/{id}`: Lanzar `404` si ID no existe.
- [ ] Endpoint `DELETE /api/v1/categorias/{id}`: Validar que no esté ya anulada, lanzar `409` si lo está (RN-04).
- [ ] Endpoint `DELETE /api/v1/categorias/{id}`: Setear `activo = false`.
- [ ] Endpoint `DELETE /api/v1/categorias/{id}`: Setear `anulado_at` con timestamp actual.
- [ ] Endpoint `DELETE /api/v1/categorias/{id}`: Retornar 204 sin borrar fila física.

### Fase 6: Módulo Productos (Schemas & Endpoints)
#### Schemas de Producto (`schema.py`)
- [ ] Crear schema `ProductoBase`.
- [ ] Definir validación Pydantic (`Field`): `nombre` con `min_length=3`.
- [ ] Definir validación Pydantic (`Field`): `precio_base` con `ge=0`.
- [ ] Definir validación Pydantic (`Field`): `stock_cantidad` con `ge=0`.
- [ ] Definir campo `unidad_venta_id` como obligatorio.
- [ ] Crear schema `ProductoCreate`.
- [ ] Definir `disponible` en `ProductoCreate`.
- [ ] Definir `stock_cantidad` en `ProductoCreate` como opcional (default 0).
- [ ] Crear schema `ProductoUpdate` con los mismos campos de Create.
- [ ] Crear schema `ProductoPublic`.
- [ ] Incluir campo anidado `unidad_venta` en `ProductoPublic`.
- [ ] Incluir lista anidada `categorias` en `ProductoPublic`.
- [ ] Incluir `stock_cantidad` en `ProductoPublic`.
- [ ] Definir propiedad/campo calculado `hay_stock` (booleano) en `ProductoPublic`.

#### Servicios y Router Productos - POST y GET (`service.py` y `router.py`)
- [ ] Endpoint `POST /api/v1/productos`: Validar `unidad_venta_id` existente (404) (RN-03).
- [ ] Endpoint `POST /api/v1/productos`: Validar nombre único entre activos (409) (RN-02).
- [ ] Endpoint `POST /api/v1/productos`: Validar stock sin decimales si unidad es contable (422) (RN-10).
- [ ] Endpoint `POST /api/v1/productos`: Persistir y retornar 201 con `response_model`.
- [ ] Endpoint `GET /api/v1/productos`: Declarar `skip` con Query(ge=0, default=0).
- [ ] Endpoint `GET /api/v1/productos`: Declarar `limit` con Query(ge=1, le=50, default=10).
- [ ] Endpoint `GET /api/v1/productos`: Implementar filtro booleano `activo` (default true).
- [ ] Endpoint `GET /api/v1/productos`: Implementar filtro booleano `disponible`.
- [ ] Endpoint `GET /api/v1/productos`: Implementar filtro entero `categoria_id` (sin duplicar filas).
- [ ] Endpoint `GET /api/v1/productos`: Implementar filtro string `search` (coincidencia parcial de nombre case-insensitive).
- [ ] Endpoint `GET /api/v1/productos`: Calcular e inyectar dinámicamente `hay_stock` en la respuesta (RN-11).
- [ ] Endpoint `GET /api/v1/productos/{id}`: Buscar por ID, 404 si no existe.
- [ ] Endpoint `GET /api/v1/productos/{id}`: Retornar 200 con `ProductoPublic` completo.

#### Servicios y Router Productos - PUT y DELETE
- [ ] Endpoint `PUT /api/v1/productos/{id}`: Lanzar 404 si el ID no existe.
- [ ] Endpoint `PUT /api/v1/productos/{id}`: Rechazar con 409 si el producto está anulado (RN-05).
- [ ] Endpoint `PUT /api/v1/productos/{id}`: Validar nombre único (409) (RN-02).
- [ ] Endpoint `PUT /api/v1/productos/{id}`: Validar stock sin decimales si unidad es contable (422) (RN-10).
- [ ] Endpoint `PUT /api/v1/productos/{id}`: Aplicar reemplazo completo de campos propios y retornar 200.
- [ ] Endpoint `DELETE /api/v1/productos/{id}`: Lanzar 404 si el ID no existe.
- [ ] Endpoint `DELETE /api/v1/productos/{id}`: Rechazar con 409 si ya está anulado (RN-04).
- [ ] Endpoint `DELETE /api/v1/productos/{id}`: Setear `activo = false`.
- [ ] Endpoint `DELETE /api/v1/productos/{id}`: Setear `anulado_at` con timestamp actual.
- [ ] Endpoint `DELETE /api/v1/productos/{id}`: Retornar 204 sin modificar `disponible` ni `stock_cantidad`.

### Fase 7: Módulo Relaciones N:N (Producto - Categoría)
- [ ] Endpoint `POST /api/v1/productos/{id}/categorias`: Recibir `categoria_id` y `es_principal` en el body.
- [ ] Endpoint `POST /api/v1/productos/{id}/categorias`: Validar existencia del producto (404).
- [ ] Endpoint `POST /api/v1/productos/{id}/categorias`: Validar existencia de la categoría (404).
- [ ] Endpoint `POST /api/v1/productos/{id}/categorias`: Rechazar con 409 si producto o categoría están anulados (RN-08).
- [ ] Endpoint `POST /api/v1/productos/{id}/categorias`: Rechazar con 409 si ya está clasificado en esa categoría (RN-07).
- [ ] Endpoint `POST /api/v1/productos/{id}/categorias`: Lógica para RN-09: si `es_principal=true`, setear la anterior categoría principal a `false`.
- [ ] Endpoint `POST /api/v1/productos/{id}/categorias`: Guardar el vínculo y retornar 201.
- [ ] Endpoint `GET /api/v1/productos/{id}/categorias`: Retornar lista de categorías del producto.
- [ ] Endpoint `GET /api/v1/productos/{id}/categorias`: Incluir indicador `es_principal` en la respuesta.

### Fase 8: Frontend - Tipos e Interfaces (TypeScript)
- [ ] Crear interface `UnidadMedida` en `src/types/`.
- [ ] Definir en `UnidadMedida`: `id`, `nombre`, `simbolo`, `tipo`.
- [ ] Crear interface `Categoria` en `src/types/`.
- [ ] Definir en `Categoria`: `id`, `nombre`, `descripcion`, `activo`, `anulado_at`.
- [ ] Crear interface `Producto` en `src/types/` (espejo de ProductoPublic).
- [ ] Definir en `Producto`: `id`, `nombre`, `descripcion`, `precio_base`.
- [ ] Definir en `Producto`: `unidad_venta` anidada (tipo `UnidadMedida`).
- [ ] Definir en `Producto`: arreglo de `categorias`.
- [ ] Definir en `Producto`: `stock_cantidad`.
- [ ] Definir en `Producto`: `disponible`, `activo`, `anulado_at`.
- [ ] Definir en `Producto`: `hay_stock` (booleano).

### Fase 9: Frontend - Componentes UI (React + Tailwind)
- [ ] Crear componente de Barra de Navegación.
- [ ] Crear componente Tarjeta/Fila de Producto.
- [ ] Renderizar en Tarjeta: Precio y símbolo de la unidad (ej. "$12,50/kg").
- [ ] Renderizar en Tarjeta: Stock y símbolo de la unidad (ej. "stock: 3,5 kg").
- [ ] Renderizar en Tarjeta: Indicador visual de `disponible`.
- [ ] Renderizar en Tarjeta: Indicador visual de `hay_stock`.
- [ ] Renderizar en Tarjeta: Botón "Editar" (con prop tipada).
- [ ] Renderizar en Tarjeta: Botón "Disponibilidad" (con prop tipada).
- [ ] Renderizar en Tarjeta: Botón "Anular" (con prop tipada).
- [ ] Aplicar estilos Tailwind utility-first a contenedor y tipografía.
- [ ] Aplicar estilos Tailwind utility-first a botones (hover, disabled).
- [ ] Crear componente Listado de Productos (recibe `Producto[]` por props).
- [ ] Implementar mapeo (`.map()`) de Tarjetas en Listado de Productos.
- [ ] Crear componente Modal de Alta/Edición.
- [ ] Configurar inputs en el Modal para nombre, descripcion, precio y stock.
- [ ] Implementar `<select>` para unidad de venta en el Modal.
- [ ] Renderizar las opciones del `<select>` iterando el estado `unidades`.

### Fase 10: Frontend - Estado Local y Lógica API (`App.tsx`)
- [ ] Crear hook `useState` para lista de `productos`.
- [ ] Crear hook `useState` para lista de `unidades`.
- [ ] Crear hook `useState` para controlar apertura del modal (`isModalOpen`).
- [ ] Crear hook `useState` para el `productoSeleccionado` (null o datos).
- [ ] Crear hook `useState` para estados de `carga` (loading).
- [ ] Crear hook `useState` para mensaje de `error`.
- [ ] Implementar `useEffect` al montar (`[]`) para ejecutar fetch a `GET /api/v1/productos`.
- [ ] Implementar `useEffect` al montar (`[]`) para ejecutar fetch a `GET /api/v1/unidades-medida`.
- [ ] Implementar estado interno en el Modal para manejar datos del formulario.
- [ ] Función limpiar formulario: inicializar vacío al crear.
- [ ] Función cargar formulario: inicializar con datos al editar.
- [ ] Implementar función fetch nativa para `POST` (Alta).
- [ ] Implementar función fetch nativa para `PUT` (Edición completa).
- [ ] Implementar función fetch nativa para `PUT` (Toggle de disponibilidad, invirtiendo booleano).
- [ ] Implementar función fetch nativa para `DELETE` (Anular producto).
- [ ] Lógica para actualizar el estado local `productos` tras cada fetch sin recargar la página.
- [ ] Lógica para cerrar el Modal al cancelar.
- [ ] Lógica para cerrar el Modal al guardar con éxito (200/201).
- [ ] Lógica para interceptar el error 409 (nombre repetido) y mostrarlo en el Modal sin cerrarlo.
- [ ] Pasar funciones (handlers) desde `App.tsx` a componentes hijos por props (levantamiento de estado).
- [ ] Renderizar indicador de carga mientras el listado espera respuesta.
- [ ] Renderizar mensaje de error general si falla el GET inicial.
- [ ] Renderizar estado "vacío" si la API retorna 0 productos.

### Fase 11: Archivos de Prueba (.http) y Entrega
#### Archivo `tests/productos.http`
- [ ] Testear `POST /api/v1/productos` válido.
- [ ] Testear `GET /api/v1/productos` básico.
- [ ] Testear `GET /api/v1/productos/{id}`.
- [ ] Testear `PUT /api/v1/productos/{id}`.
- [ ] Testear `DELETE /api/v1/productos/{id}`.
- [ ] Testear filtro `activo` en GET.
- [ ] Testear filtro `disponible` en GET.
- [ ] Testear filtro `categoria_id` en GET.
- [ ] Testear filtro `search` en GET.
- [ ] Simular error 404 (ID inexistente).
- [ ] Simular error 409 (nombre repetido).
- [ ] Simular error 409 (anular un producto ya anulado).
- [ ] Simular error 422 (stock negativo).
- [ ] Simular error 422 (stock con decimales en unidad contable).
- [ ] Validar indicador `hay_stock` leyendo producto, actualizando stock a 0 y volviendo a leer.

#### Archivo `tests/relaciones.http`
- [ ] Testear alta de categorías `POST /api/v1/categorias`.
- [ ] Simular error 409 al crear categoría con nombre repetido.
- [ ] Testear anulación de categoría `DELETE` y verificar (con un `GET`) que sus productos siguen activos.
- [ ] Testear vinculación producto-categoría `POST /api/v1/productos/{id}/categorias`.
- [ ] Simular error 409 al clasificar un producto dos veces en la misma categoría.
- [ ] Testear clasificar producto en nueva categoría enviando `es_principal = true` y verificar cambio.

#### Condiciones Finales de Entrega
- [ ] Comprobar que en `app/core/database.py` esté expuesta la cadena de conexión configurada.
- [ ] Escribir pasos de instalación y ejecución en `foodstore-backend/README.md`.
- [ ] Escribir comandos de instalación y ejecución en `foodstore-frontend/README.md`.
- [ ] Borrar carpeta `__pycache__/` en backend.
- [ ] Borrar carpeta `.venv/` en backend.
- [ ] Borrar carpeta `node_modules/` en frontend.
- [ ] Borrar carpeta `dist/` en frontend.
- [ ] Comprimir ambas carpetas raíz (`foodstore-backend/` y `foodstore-frontend/`) en `Apellido_Nombre_P2.zip`.