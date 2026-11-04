# Food Store - Backend

Backend desarrollado por Matias Manuel Carro para el Segundo Parcial de Programación IV.

El proyecto implementa una API REST para administrar un catálogo de productos, categorías, unidades de medida y las relaciones entre productos y categorías.

## Tecnologías

- Python 3.12+
- FastAPI
- SQLModel
- Pydantic v2
- PostgreSQL 15+
- Psycopg
- Uvicorn

## Requisitos previos

Antes de ejecutar el proyecto es necesario tener instalado:

- Python 3.12 o superior
- PostgreSQL 15 o superior

## Base de datos

Crear en PostgreSQL una base de datos llamada:

```sql
CREATE DATABASE "2do_parcial_prog4";
```

La conexión se configura en:

```text
app/core/database.py
```

Actualmente:

```python
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/2do_parcial_prog4"
```

Modificar usuario, contraseña, host o puerto si la configuración local de PostgreSQL es diferente.

## Instalación

Desde la carpeta `backend`, crear un entorno virtual:

```powershell
python -m venv .venv
```

Activarlo:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

## Ejecución

Desde la carpeta `backend`:

```powershell
fastapi dev app/main.py
```

La API estará disponible en:

```text
http://127.0.0.1:8000
```

La documentación Swagger estará disponible en:

```text
http://127.0.0.1:8000/docs
```

También se incluye `run.py` como alternativa para desarrollo:

```powershell
python run.py
```

## Seed inicial

Al iniciar la aplicación se crean las tablas necesarias y se ejecuta el seed de unidades de medida.

El seed solamente inserta los registros si la tabla de unidades está vacía.

Unidades iniciales:

- kilogramo (`kg`) - peso
- gramo (`g`) - peso
- litro (`L`) - volumen
- mililitro (`mL`) - volumen
- pieza (`u`) - contable
- docena (`doc`) - contable

## Endpoints

Todos los endpoints utilizan el prefijo:

```text
/api/v1
```

### Unidades de medida

| Método | Endpoint                   | Descripción                              |
| ------ | -------------------------- | ---------------------------------------- |
| GET    | `/api/v1/unidades-medida/` | Listar el catálogo de unidades de medida |

Las unidades de medida son un catálogo de solo lectura.

### Categorías

| Método | Endpoint                  | Descripción                               |
| ------ | ------------------------- | ----------------------------------------- |
| POST   | `/api/v1/categorias/`     | Crear una categoría                       |
| GET    | `/api/v1/categorias/`     | Listar categorías                         |
| GET    | `/api/v1/categorias/{id}` | Obtener una categoría por ID              |
| PUT    | `/api/v1/categorias/{id}` | Actualizar nombre y descripción           |
| DELETE | `/api/v1/categorias/{id}` | Anular una categoría mediante baja lógica |

El listado de categorías admite los siguientes filtros:

- `activo`: filtra categorías activas o anuladas.
- `search`: realiza una búsqueda parcial por nombre.

### Productos

| Método | Endpoint                 | Descripción                                |
| ------ | ------------------------ | ------------------------------------------ |
| POST   | `/api/v1/productos/`     | Crear un producto                          |
| GET    | `/api/v1/productos/`     | Listar productos                           |
| GET    | `/api/v1/productos/{id}` | Obtener un producto por ID                 |
| PUT    | `/api/v1/productos/{id}` | Actualizar los campos propios del producto |
| DELETE | `/api/v1/productos/{id}` | Anular un producto mediante baja lógica    |

El listado de productos admite los siguientes parámetros:

- `skip`: cantidad de registros a omitir. Valor por defecto: `0`.
- `limit`: cantidad máxima de registros. Valor por defecto: `10`, máximo: `50`.
- `activo`: filtra productos activos o anulados.
- `disponible`: filtra según disponibilidad de venta.
- `categoria_id`: filtra productos pertenecientes a una categoría.
- `search`: realiza una búsqueda parcial por nombre.

### Relación Producto - Categoría

| Método | Endpoint                            | Descripción                                                         |
| ------ | ----------------------------------- | ------------------------------------------------------------------- |
| POST   | `/api/v1/productos/{id}/categorias` | Clasificar un producto en una categoría                             |
| GET    | `/api/v1/productos/{id}/categorias` | Listar las categorías de un producto indicando cuál es la principal |

La clasificación recibe un cuerpo con la siguiente estructura:

```json
{
  "categoria_id": 1,
  "es_principal": true
}
```

Un producto puede pertenecer a varias categorías, pero solamente una puede estar marcada como principal.

## Stock

Cada producto almacena su propio `stock_cantidad`.

El campo `hay_stock` no se persiste en la base de datos. Se calcula al devolver el producto:

```text
hay_stock = stock_cantidad > 0
```

Para unidades de tipo `contable`, el stock debe ser un número entero.

## Baja lógica

Los productos y categorías no se eliminan físicamente.

Al realizar la baja se modifican:

```text
activo = false
anulado_at = fecha y hora actual
```

De esta manera los registros conservan su información histórica.

## Pruebas

Los archivos de prueba se encuentran en:

```text
app/tests/
```

### Productos

```text
app/tests/productos.http
```

Incluye pruebas de:

- Alta de productos.
- Listado.
- Consulta por ID.
- Actualización.
- Baja lógica.
- Paginación.
- Filtros.
- Nombre repetido.
- IDs inexistentes.
- Unidad de medida inexistente.
- Precio negativo.
- Stock negativo.
- Stock decimal para unidades contables.
- Cálculo de `hay_stock`.
- Disponibilidad.
- Modificación y anulación de registros anulados.

### Relaciones

```text
app/tests/relaciones.http
```

Incluye pruebas de:

- Alta de categorías.
- Nombre de categoría repetido.
- Clasificación de productos.
- Clasificación duplicada.
- Categoría principal.
- Cambio de categoría principal.
- Filtro por categoría.
- Anulación de categorías.
- Independencia entre el estado de categorías y productos.
- Clasificación con producto o categoría anulados.
- Categoría inexistente.

## Estructura principal

```text
app/
├── core/
│   ├── database.py
│   └── seed.py
├── modules/
│   ├── categorias/
│   ├── productos/
│   └── unidades_medida/
├── tests/
│   ├── productos.http
│   └── relaciones.http
└── main.py
```

### Desarrolado por Matias Manuel Carro
