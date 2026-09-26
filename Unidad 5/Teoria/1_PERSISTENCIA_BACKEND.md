

# 1. 🧱 Arquitectura Modular para FastAPI + SQLModel + PostgreSQL

Esta es la estructura recomendada para un backend profesional con FastAPI,
SQLModel y PostgreSQL, separando claramente las capas:

- Router → expone endpoints HTTP
- Service → lógica de negocio
- Schema → entrada/salida de la API (Pydantic)
- Model → persistencia real (SQLModel → PostgreSQL)
  
## Estructura del proyecto

```powershell
app/
│
├── database.py
├── main.py
│
├── models/
│   ├── producto.py
│   ├── categoria.py
│   └── proveedor.py
│
├── schemas/
│   ├── producto.py
│   ├── categoria.py
│   └── proveedor.py
│
├── services/
│   ├── producto.py
│   ├── categoria.py
│   └── proveedor.py
│
└── routers/
    ├── producto.py
    ├── categoria.py
    └── proveedor.py

```


---

# 🧩 ¿Qué hace cada archivo?

---

## 1️⃣ `models.py` → **Persistencia (SQLModel / Tablas)**

Representa **la estructura real en PostgreSQL**.

- Define tablas  
- Columnas  
- Tipos  
- Relaciones  
- Foreign keys  

Ejemplo:

```python
from sqlmodel import SQLModel, Field

class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    categoria_id: int = Field(foreign_key="categoria.id")
    proveedor_id: int = Field(foreign_key="proveedor.id")
    precio: float
    stock: int
    stock_minimo: int
    activo: bool = True
```

---

## 2️⃣ `schemas.py` → **Contratos de API (Pydantic)**

Define **qué recibe y qué devuelve la API**.

- Validaciones  
- Ejemplos  
- Modelos de entrada (POST/PUT)  
- Modelos de salida (GET)  

Ejemplo:

```python
from pydantic import BaseModel

class ProductoBase(BaseModel):
    nombre: str
    categoria_id: int
    proveedor_id: int
    precio: float
    stock: int
    stock_minimo: int
    activo: bool = True

class ProductoCreate(ProductoBase):
    pass

class ProductoRead(ProductoBase):
    id: int
```

---

## 3️⃣ `services.py` → **Lógica de negocio**

Acá va lo que realmente hace tu API:

- Crear producto  
- Actualizar stock  
- Validar reglas  
- Consultar base  
- Manejar transacciones  

Ejemplo:

```python
from .models import Producto

def crear_producto(data, session):
    producto = Producto(**data.dict())
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto
```

---

## 4️⃣ `routers.py` → **Endpoints HTTP**

Expone las rutas:

- GET /productos  
- POST /productos  
- PUT /productos/{id}  
- DELETE /productos/{id}  

Ejemplo:

```python
from fastapi import APIRouter
from .schemas import ProductoCreate, ProductoRead
from .services import crear_producto
from app.database import SessionDep

router = APIRouter(prefix="/productos")

@router.post("/", response_model=ProductoRead)
def crear_producto_endpoint(data: ProductoCreate, session: SessionDep):
    return crear_producto(data, session)
```

---

# 🟦 Archivos globales

---

## `database.py` → Engine + Sesión + create_all()

- URL de conexión a PostgreSQL  
- Engine global  
- Sesión por request  
- Creación de tablas  

Ejemplo:

```python
from sqlmodel import SQLModel, create_engine, Session

engine = create_engine("postgresql+psycopg://postgres:1234@localhost:5432/mi_db")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

---

## `main.py` → Registro de routers

Ejemplo:

```python
from fastapi import FastAPI
from app.producto.routers import router as producto_router
from app.proveedor.routers import router as proveedor_router
from app.categoria.routers import router as categoria_router
from app.database import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def startup():
    create_db_and_tables()

app.include_router(producto_router)
app.include_router(proveedor_router)
app.include_router(categoria_router)
```

---

## 🎯 Resumen

| Archivo | Rol | Qué contiene |
|--------|------|--------------|
| **models.py** | Persistencia | Tablas SQLModel (PostgreSQL) |
| **schemas.py** | API | Pydantic (entrada/salida JSON) |
| **services.py** | Lógica | Funciones que operan sobre la BD |
| **routers.py** | HTTP | Endpoints que llaman a services |
| **database.py** | Infraestructura | Engine, sesión, create_all |
| **main.py** | App | Registro de routers |

---
---

# Teoría: ¿Cuál es “el objeto” en FastAPI + SQLModel?

Cuando venís de Java/Spring, tu referencia mental es:

- Una **clase Producto** (objeto de dominio)
- Un **DTO** (objeto que viaja por la API)
- Un **Service** (lógica)
- Un **Controller** (endpoints)

FastAPI + SQLModel funciona igual, solo que con otros nombres.

---

# 🧩 Resumen Ultra Claro

### ✔ El “objeto” de tu dominio → **Model (SQLModel)**
Representa la **tabla real** en la base de datos.  
Es equivalente a una **Entity JPA** en Java.

Ejemplo conceptual:

```python
class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    precio: float
```

Este objeto **vive en la BD**, tiene columnas, tipos, relaciones, foreign keys.

---

### ✔ El “objeto” que viaja por la API → **Schema (Pydantic)**
Representa **lo que entra y sale** por la API en formato JSON.  
Es equivalente a un **DTO** en Java.

Ejemplo conceptual:

```python
class ProductoCreate(BaseModel):
    nombre: str
    precio: float

class ProductoRead(ProductoCreate):
    id: int
```

Este objeto **no toca la BD**, solo valida y define contratos de API.

---

### ✔ Que ejecuta las reglas → **Service**
Representa la **lógica de negocio**.

Ejemplo conceptual:

```python
def crear_producto(data: ProductoCreate, session):
    producto = Producto(**data.dict())
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto
```

Este objeto **usa Models**, **recibe Schemas**, y **aplica reglas**.

---

### ✔ Que expone las rutas → **Router**
Representa los **endpoints HTTP**.

Ejemplo conceptual:

```python
@router.post("/", response_model=ProductoRead)
def crear_producto_endpoint(data: ProductoCreate, session):
    return crear_producto(data, session)
```

Este objeto **no tiene lógica**, solo conecta la API con los Services.

---

# 🧠 Mapa mental (equivalencia con Java)

| Concepto | Java / Spring | FastAPI / SQLModel |
|---------|----------------|--------------------|
| Objeto de dominio | Entity | Model (SQLModel) |
| Objeto que viaja por la API | DTO | Schema (Pydantic) |
| Lógica | Service | Service |
| Endpoints | Controller | Router |

---

# 🎯 Conclusión

En FastAPI + SQLModel:

- **Model** = tu clase “Producto” de Java (objeto de dominio real)
- **Schema** = tu DTO (objeto que viaja por la API)
- **Service** = tu lógica (reglas, persistencia, validaciones)
- **Router** = tu controller (endpoints HTTP)


---
---

# Flujo de la Base de Datos  
## Estructura y responsabilidad de `database.py`

La capa de persistencia es el punto donde FastAPI se conecta con PostgreSQL.  
Su función es **centralizar la configuración del motor**, **crear las tablas** y **proveer sesiones por request**.

Este flujo es fundamental para entender cómo viaja un dato desde el cliente hasta la base, y cómo vuelve convertido en una respuesta.

---

# 🔄 2. Flujo completo de la operación en FastAPI + SQLModel + PostgreSQL

```
Cliente
→ Endpoint (Router)
→ Modelo de entrada (Schema)
→ Lógica (Service)
→ Modelo DB (SQLModel)
→ Session
→ Engine
→ PostgreSQL
→ Commit
→ Modelo público (Schema de salida)
→ Respuesta HTTP
```

---

# 🧩 Explicación de cada etapa del flujo

## 1. Cliente  
Puede ser:  
- un navegador  
- un frontend React/Vue/Angular  
- un script Python  
- un cliente móvil  

Envía una petición HTTP (GET, POST, PUT, DELETE).

---

## 2. Endpoint (Router)  
El router recibe la petición y decide **qué función del backend** debe ejecutarse.

Ejemplo:

```python
@router.post("/", response_model=ProductoRead)
def crear_producto(data: ProductoCreate, session: SessionDep):
    return crear_producto(data, session)
```

Responsabilidad:  
- Validar que el request coincida con el Schema  
- Llamar al Service  
- Devolver el Schema de salida  

---

## 3. Modelo de entrada (Schema – Pydantic)  
El Schema valida el JSON recibido.

Responsabilidad:  
- Garantizar tipos correctos  
- Validar reglas simples (ej: precio > 0)  
- Proteger la API de datos inválidos  

---

## 4. Lógica (Service)  
El Service ejecuta la lógica de negocio.

Responsabilidad:  
- Crear objetos SQLModel  
- Consultar la base  
- Aplicar reglas  
- Manejar transacciones  

Ejemplo conceptual:

```python
def crear_producto(data: ProductoCreate, session):
    producto = Producto(**data.dict())
    session.add(producto)
    session.commit()
    session.refresh(producto)
    return producto
```

---

## 5. Modelo DB (SQLModel)  
Es el **objeto de dominio**, equivalente a una Entity en Java.

Responsabilidad:  
- Representar la tabla  
- Definir columnas  
- Definir relaciones  
- Ser persistible  

---

## 6. Session  
La sesión es el canal que permite ejecutar operaciones SQL.

Responsabilidad:  
- Insertar  
- Actualizar  
- Consultar  
- Eliminar  
- Manejar transacciones  

---

## 7. Engine  
El engine es la conexión física a PostgreSQL.

Responsabilidad:  
- Abrir conexiones  
- Ejecutar SQL  
- Crear tablas (via `create_all`)  

---

## 8. PostgreSQL  
La base de datos almacena los datos de forma persistente.

Responsabilidad:  
- Guardar registros  
- Mantener integridad  
- Ejecutar constraints  
- Responder consultas  

---

## 9. Commit  
Confirma la operación en la base.

Responsabilidad:  
- Persistir cambios  
- Garantizar atomicidad  

---

## 10. Modelo público (Schema de salida)  
Convierte el objeto SQLModel en un JSON limpio para el cliente.

Responsabilidad:  
- Ocultar campos internos  
- Formatear la respuesta  
- Garantizar consistencia del contrato de API  

---

## 11. Respuesta HTTP  
El backend devuelve un JSON válido, listo para ser consumido por el cliente.

---
---

## 🔗 El Engine (Motor de Conexión)

El **engine** es el objeto central que administra las conexiones entre FastAPI y PostgreSQL.  
Toda la aplicación debe usar **una única instancia global** del engine para garantizar consistencia, eficiencia y evitar fugas de conexión.

---

### 🧩2.  ¿Qué hace el engine?

- Abre conexiones hacia PostgreSQL.  
- Ejecuta las consultas SQL generadas por SQLModel/SQLAlchemy.  
- Administra el pool de conexiones.  
- Se usa indirectamente a través de las sesiones (`Session`).  
- Permite crear las tablas mediante `SQLModel.metadata.create_all(engine)`.

El engine **no ejecuta lógica de negocio**, **no valida datos**, **no maneja rutas**.  
Su única responsabilidad es ser el puente técnico hacia la base de datos.

---

## 🛠️ Configuración típica con PostgreSQL

```python
from sqlmodel import create_engine
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://user:password@localhost:5432/database_name"
)

engine = create_engine(DATABASE_URL, echo=True)
```

---

## 🔍 Explicación de cada parte

### **1. `postgresql+psycopg`**
Indica:

- **postgresql** → el dialecto SQL que se va a usar.  
- **psycopg** → el driver que permite a Python comunicarse con PostgreSQL.

Es equivalente a decir:  
“Usá PostgreSQL y conectate usando el driver psycopg”.

---

### **2. `echo=True`**
Activa el modo de depuración del engine.

Cuando está en `True`, cada consulta SQL generada por SQLModel/SQLAlchemy se imprime en la consola.

Sirve para:

- Ver qué SQL se ejecuta realmente.  
- Depurar errores de consultas.  
- Entender cómo SQLModel traduce tus modelos a SQL.

En producción se recomienda desactivarlo (`echo=False`).

---

### **3. Variables de entorno**
Usar:
```python
os.getenv("DATABASE_URL")
```

permite:

- No exponer credenciales en el código.  
- Cambiar la base sin modificar archivos Python.  
- Usar configuraciones distintas para desarrollo, testing y producción.

Ejemplo de variable de entorno:

```python
DATABASE_URL=postgresql+psycopg://postgres:1234@localhost:5432/mi_db
```

---
---


## 2.2 Creación de Tablas

Para que los modelos definidos en código (SQLModel con `table=True`) se reflejen en la base de datos, FastAPI necesita ejecutar una función que inspeccione todos los modelos y genere las tablas correspondientes.

La forma estándar de hacerlo es:

```python
from sqlmodel import SQLModel

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```

---

# 🧩 ¿Qué hace esta función?

### 1. Inspección de modelos
SQLModel revisa todos los modelos declarados en tu proyecto que tengan:

```python
table=True
```


Ejemplo conceptual:

```python
class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
```

SQLModel detecta automáticamente:

- columnas  
- tipos  
- claves primarias  
- claves foráneas  
- índices  

---

### 2. Generación de SQL
A partir de los modelos, SQLModel construye las sentencias SQL necesarias:

- `CREATE TABLE`  
- `CREATE INDEX`  
- `ALTER TABLE` para claves foráneas  

Estas sentencias se generan internamente usando SQLAlchemy.

---

### 3. Creación de tablas en PostgreSQL
El engine ejecuta las sentencias SQL generadas.  
Si las tablas **no existen**, se crean.  
Si ya existen, **no se modifican** (no hace migraciones).

Esto garantiza que tu base de datos queda sincronizada con tus modelos.

---

# 🚀 ¿Cuándo se ejecuta esta función?

Normalmente en el evento `startup` de FastAPI:

```python
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
```

Esto asegura que:

- La base está lista antes de recibir peticiones.  
- Todas las tablas existen desde el inicio.  
- No tenés que crear tablas manualmente en PostgreSQL.

---

# 🎯 Conclusión

`create_db_and_tables()` es el puente entre tus modelos SQLModel y la base de datos.  
Su responsabilidad es:

- inspeccionar modelos  
- generar SQL  
- crear tablas si no existen  

Es una pieza fundamental de la capa de persistencia y se ejecuta una sola vez al iniciar la aplicación.

---
---

# 2.3 🧩 La Sesión (Session)

La **Session** representa una transacción activa entre tu aplicación y la base de datos.  
Es el objeto que permite ejecutar operaciones SQL de forma controlada y segura.

La sesión es el componente que conecta la lógica de negocio con el engine, y administra el ciclo de vida de los cambios en la base.

---

## Responsabilidades de la Session

### ✔ Mantener objetos en memoria  
Cuando cargás un registro desde la base, la sesión mantiene una copia del objeto en memoria.  
Esto permite detectar cambios sin necesidad de escribir SQL manual.

---

### ✔ Detectar cambios (Dirty Checking)  
Si modificás un atributo de un modelo SQLModel, la sesión detecta automáticamente que el objeto cambió.

Ejemplo conceptual:

```python
producto.precio = 1200
```

La sesión registra este cambio y lo aplicará en el próximo `commit()`.

---

### ✔ Ejecutar transacciones  
Todas las operaciones de escritura (INSERT, UPDATE, DELETE) se ejecutan dentro de una transacción.

Esto garantiza:

- atomicidad  
- consistencia  
- rollback seguro en caso de error  

---

### ✔ Confirmar (commit)  
`commit()` envía los cambios a PostgreSQL de manera permanente.

Hasta que no se ejecuta `commit()`, **nada queda guardado**.

---

### ✔ Revertir (rollback)  
Si ocurre un error, la sesión puede revertir la transacción completa.

Esto evita que la base quede en un estado inconsistente.

---

# 🔑 Concepto clave

### **Mientras no se ejecute `commit()`, los cambios no son permanentes.**

Podés:

- crear objetos  
- modificarlos  
- eliminarlos  

Pero **nada se guarda** hasta que la sesión confirma la transacción.

---

# 🛠️ Ejemplo conceptual de uso

```python
with Session(engine) as session:
    producto = Producto(nombre="Silla", precio=100)
    session.add(producto)
    session.commit()   # recién aquí se guarda en PostgreSQL
    session.refresh(producto)
```

---

# 🎯 Conclusión

La Session es el componente que:

- administra transacciones  
- detecta cambios  
- ejecuta operaciones SQL  
- confirma o revierte modificaciones  

Sin sesión, no hay persistencia.  
Sin commit, no hay cambios permanentes.

---
---

# 🔧 3. Modelos Segregados (Separación de Responsabilidades)

En una arquitectura profesional, **el frontend nunca debe interactuar directamente con los modelos de base de datos**.  
Los modelos SQLModel representan la estructura interna de la BD y pueden contener campos sensibles, internos o no destinados al cliente.

Para evitar acoplamiento y problemas de seguridad, se separan los modelos en tres niveles:

- Modelo base compartido  
- Modelo de tabla (persistencia)  
- Modelos de entrada y salida (API)

Esta segregación cumple principios esenciales:

- Separación de capas  
- Responsabilidad única  
- Desacople entre API y almacenamiento  
- Evolución independiente de la API y la BD  

---

# 3.1 Clase Base

La clase base contiene los campos comunes que comparten los distintos modelos, pero **no representa una tabla**.  
Sirve como estructura reutilizable.

Ejemplo:

```python
from sqlmodel import Field, SQLModel

class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
```

Características:

- No tiene `table=True`.  
- No crea tablas.  
- Solo define atributos comunes.  
- Se usa como base para modelos de tabla y modelos de API.

---

# 3.2 Modelo de Tabla (Persistencia)

Este modelo **sí representa una entidad persistida en PostgreSQL**.  
Incluye campos internos, claves primarias y cualquier dato que no debe exponerse públicamente.

Ejemplo:

```python
from typing import Optional
from sqlmodel import SQLModel, Field

class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None
```

Características:

- `table=True` → se mapeará a una tabla real.  
- `id` → clave primaria autogenerada.  
- Puede incluir campos internos como `secret_name`.  
- No debe usarse directamente como entrada/salida en la API.

---

# 3.3 Modelos de Datos (API)

Los modelos de API son los que **viajan entre el cliente y el servidor**.  
Nunca deben ser los mismos que los modelos de tabla.

Razones fundamentales:

### 1. Seguridad  
No todos los campos deben exponerse.  
Ejemplo: `secret_name` jamás debería aparecer en un JSON público.

### 2. Control  
El cliente no debe poder modificar campos críticos como:

- `id`  
- claves foráneas  
- flags internos  
- estados del sistema  

### 3. Evolución  
La API puede cambiar sin afectar la estructura interna de la base.  
Esto permite:

- versionar endpoints  
- agregar campos públicos  
- ocultar campos internos  
- mantener compatibilidad hacia atrás  

Ejemplo conceptual de modelos API:

```python
class HeroCreate(HeroBase):
    secret_name: str

class HeroRead(HeroBase):
    id: int
```

---


# 🎯 Conclusión

Separar los modelos en tres niveles garantiza:

- Seguridad  
- Orden  
- Escalabilidad  
- Independencia entre API y BD  
- Código limpio y mantenible  

El frontend interactúa solo con **Schemas (Pydantic)**.  
La base de datos interactúa solo con **Models (SQLModel)**.  
La lógica de negocio une ambos mundos sin mezclarlos.


# 3.4 Modelos específicos según la interacción del cliente

Para evitar exponer la estructura interna de la base de datos y mantener una arquitectura segura y desacoplada, se definen **modelos distintos** para cada tipo de operación de la API.

Estos modelos actúan como filtros y contratos, asegurando que el cliente solo vea y modifique lo que corresponde.

---

# 🟦 Modelo de creación — `HeroCreate`

Este modelo representa **los datos que el cliente debe enviar para crear un recurso**.

Características:

- Incluye solo los campos necesarios para registrar la entidad.
- **No incluye el identificador**, porque la base de datos lo genera automáticamente.
- Permite controlar qué campos son obligatorios y cuáles opcionales.

Ejemplo conceptual:

```python
class HeroCreate(HeroBase):
    secret_name: str
```

---

# 🟦 Modelo público — `HeroPublic`

Este modelo define **qué información se devuelve al cliente**.

Características:

- Incluye el `id` generado por la base.
- Excluye campos sensibles como `secret_name`.
- Actúa como un filtro entre la base de datos y el exterior.

Ejemplo conceptual:

```python
class HeroPublic(HeroBase):
    id: int
```

De esta forma, aunque el modelo de tabla contenga información privada, la API solo expone lo permitido.

---

# 🟦 Modelo de actualización — `HeroUpdate`

Este modelo se utiliza para operaciones **PATCH** (actualizaciones parciales).

Características:

- Todos los campos son opcionales.
- El sistema solo modifica los campos enviados explícitamente.
- Permite actualizaciones flexibles sin obligar al cliente a reenviar toda la entidad.

Ejemplo conceptual:

```python
class HeroUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
```

---

# 🔄 Flujo conceptual completo

```
Cliente envía datos
→ Se validan con un modelo de entrada (Create / Update)
→ Se transforman en un modelo de base de datos (SQLModel)
→ Se guardan en PostgreSQL
→ Se devuelve un modelo público filtrado (Public)
```


Este diseño garantiza que:

- La estructura interna de la base **no queda expuesta**.
- La API puede evolucionar sin afectar la base de datos.
- El cliente solo interactúa con los campos permitidos.
- La seguridad y el control están asegurados.

---

# 🎯 Conclusión

Separar los modelos en:

- **Create** → entrada controlada  
- **Public** → salida filtrada  
- **Update** → modificaciones parciales  

permite construir una API robusta, segura y desacoplada de la estructura interna de la base de datos.

---
---

# 📁 4. Flujo DB en las Rutas (APIRouter)

FastAPI permite organizar endpoints usando `APIRouter`, lo que facilita separar módulos, agrupar rutas y mantener una arquitectura limpia.

Ejemplo básico:

```python
from fastapi import APIRouter

router = APIRouter(prefix="/heroes", tags=["heroes"])
```

---

# 4.1 Creación de Registros (POST)

Este endpoint recibe datos del cliente, los valida, los transforma en un modelo de tabla y los persiste en la base de datos.

```python
@router.post("/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero
```

---

## 🔄 Flujo técnico paso a paso

1. **Se recibe `HeroCreate`**  
   El cliente envía un JSON que se valida automáticamente.

2. **Se transforma en modelo de tabla (`Hero`)**  
   `model_validate()` convierte el Schema en un SQLModel listo para persistir.

3. **`session.add()` registra el objeto**  
   La sesión marca el objeto como “pendiente” para inserción.

4. **`commit()` ejecuta la transacción**  
   Se envía el `INSERT` real a PostgreSQL.

5. **`refresh()` sincroniza el objeto**  
   Se actualiza con datos generados por la BD (ej: `id` autoincremental).

6. **`response_model` filtra datos sensibles**  
   Solo se devuelven los campos definidos en `HeroPublic`.

---

# 4.2 Actualización Parcial (PATCH)

Diferencia conceptual:

- **PUT** → reemplaza completamente el recurso.  
- **PATCH** → modifica solo los campos enviados.

Ejemplo:

```python
from fastapi import HTTPException

@router.patch("/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")

    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)

    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)

    return hero_db
```

---

## 🔍 Conceptos clave

### ✔ `exclude_unset=True`
Evita sobrescribir campos que el cliente **no envió**.  
Solo se actualizan los valores presentes en el JSON.

### ✔ `sqlmodel_update()`
Aplica los cambios al modelo de tabla sin reemplazarlo completo.

### ✔ `session.get()`
Busca el registro por su `id`.  
Si no existe, se devuelve un error 404.

### ✔ `session.commit()` y `session.refresh()`
Confirman la transacción y sincronizan el objeto actualizado.

---

# 🔄 Flujo técnico del PATCH

```
Cliente envía datos parciales
→ Schema HeroUpdate valida los campos enviados
→ Se obtiene el registro existente
→ Se actualizan solo los campos presentes
→ Se guarda la transacción
→ Se devuelve HeroPublic filtrado
```


---

# 🎯 Conclusión

El uso de modelos segregados + APIRouter + Session permite:

- Control total sobre qué datos entran y salen  
- Actualizaciones seguras y parciales  
- Persistencia confiable  
- Separación clara entre API, lógica y base de datos  
- Evitar exponer la estructura interna de la BD  

---
---

# 5. Transacciones y Manejo de Errores

Una **Session** gestiona una **transacción**, y toda transacción en PostgreSQL cumple cuatro propiedades fundamentales:

### ✔ Atomicidad  
La operación es “todo o nada”.  
Si algo falla, **ningún cambio parcial queda aplicado**.

### ✔ Consistencia  
La base mantiene sus reglas de integridad:  
- claves primarias  
- claves foráneas  
- constraints  
- tipos de datos  

### ✔ Aislamiento  
Las transacciones no interfieren entre sí.  
Lo que ocurre dentro de una sesión no afecta a otras hasta que se hace commit.

### ✔ Durabilidad  
Una vez ejecutado `commit()`, los cambios quedan **permanentes** en la base.

---

## 🛠️ Ejemplo con rollback

Cuando ocurre un error, es obligatorio revertir la transacción para evitar dejar la base en un estado inconsistente.

```python
try:
    session.commit()
except Exception:
    session.rollback()
    raise
```

Esto garantiza que:

- no queden datos corruptos  
- no se apliquen cambios parciales  
- la base mantenga su integridad  

---
---


# 6. Relaciones entre Modelos

La persistencia real incluye **relaciones entre tablas**.  
SQLModel permite definir relaciones usando `Relationship()`.

Ejemplo de relación **uno a muchos**:

```python
from sqlmodel import Relationship

class Team(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    heroes: list["Hero"] = Relationship(back_populates="team")

class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    team_id: int | None = Field(default=None, foreign_key="team.id")
    team: Team | None = Relationship(back_populates="heroes")
```

---

## 🔍 Conceptos clave

### ✔ `foreign_key`
Define la integridad referencial.  
Ejemplo: `team_id` debe apuntar a un `Team.id` válido.

### ✔ `Relationship()`
Permite navegar entre objetos:

- `team.heroes` → lista de héroes del equipo  
- `hero.team` → equipo al que pertenece el héroe  

Esto facilita consultas y evita escribir SQL manual.

### ✔ PostgreSQL asegura coherencia
La base garantiza que:

- no existan héroes con `team_id` inexistente  
- no se eliminen equipos referenciados sin manejar la relación  
- las claves foráneas mantengan integridad  

---

# 🎯 Conclusión

Las transacciones aseguran que la base esté siempre consistente, y las relaciones permiten modelar estructuras reales sin exponer SQL manual.  
Combinando Session + commit/rollback + relaciones, obtenés una capa de persistencia sólida, segura y profesional.

