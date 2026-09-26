# CRUD Persistente — Documento Resumido y Profesional

Este documento resume el flujo completo de un CRUD persistente en FastAPI + SQLModel + PostgreSQL, siguiendo una arquitectura modular y segura.

---

# 1. ¿Qué es un CRUD Persistente?

Un CRUD persistente crea, lee, actualiza y elimina datos de forma segura en una base de datos.

Resuelve problemas clásicos:

- Pérdida de datos al reiniciar el servidor  
- Inconsistencias por falta de validación  
- Exposición de datos sensibles  

El objetivo es una arquitectura robusta, segura y mantenible.

---

# 2. Flujo Central de Datos

Flujo obligatorio:

    Request → Validación → Commit (Transacción) → Response Model

Saltarse una etapa es una falla de seguridad.

---

## 2.1 Request (Entrada)

El cliente envía una petición HTTP:

- Verbos: POST, GET, PUT, PATCH, DELETE  
- Datos en JSON  
- Información no confiable por defecto  

---

## 2.2 Validación (Schemas)

Antes de tocar la base:

- Se validan tipos  
- Se validan reglas de negocio  
- Se rechaza temprano con error 400  
- Se usan Schemas como contrato de entrada  

Ejemplo:

```python
class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    stock: int
```

---

## 2.3 Commit (Persistencia real)

Una vez validados los datos:

- Se ejecuta la transacción  
- Atomicidad: todo o nada  
- Rollback si hay error  
- Commit si todo es correcto  

Ejemplo:

```python
try:
    session.commit()
except Exception:
    session.rollback()
    raise
```

---

## 2.4 Response Model (Salida filtrada)

Nunca se devuelve el modelo de base de datos crudo.

Ventajas:

- Oculta datos sensibles  
- Formatea la salida  
- Mantiene un contrato estable  

Ejemplo:

```python
class ProductoResponse(BaseModel):
    id: int
    nombre: str
    precio: float
```

---

# 3. Estructura del Proyecto

```powershell
nombre-proyecto/
│
├── main.py
├── database.py
│
└── app/
    ├── routers/   → Maneja Requests
    ├── schemas/   → Validación + Response Models
    ├── models/    → Tablas de BD
    └── service/   → Lógica + Transacciones
```
---

# 4. Implementación Paso a Paso

## Paso 1 — Schemas (Entrada y Salida)

```python
class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    stock: int

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    precio: float
```

---

## Paso 2 — Modelo de Base de Datos

```python
class Producto(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    precio: float
    stock: int
```

---

## Paso 3 — Service (Transacción)

```python
def crear_producto(session: Session, data: ProductoCreate) -> Producto:
    nuevo = Producto(**data.model_dump())
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo
```

---

## Paso 4 — Router (Request)

```python
@app.post("/productos/", response_model=ProductoResponse)
def endpoint_crear_producto(producto: ProductoCreate, db: Session):
    creado = crear_producto(db, producto)
    return creado
```

---

# 5. Buenas Prácticas

- ✅ Separar modelos de entrada y salida  
- ✅ Nunca hacer commit en el router  
- ✅ Usar transacciones con rollback  
- ✅ Mantener los endpoints limpios  
- ✅ Tipar todo  

---

# 6. Errores Comunes

- ❌ Recibir JSON sin validarlo  
- ❌ Hacer commit en el router  
- ❌ Devolver el modelo de BD completo  
- ❌ Confundir ORM con Schema  

---

# 7. Conclusión

El flujo:

    Request → Validación → Service (Transacción) → Response Model

es el estándar profesional.  
Garantiza seguridad, persistencia confiable, escalabilidad y arquitectura limpia.

Primero la integridad de los datos.  
Después las funcionalidades.

