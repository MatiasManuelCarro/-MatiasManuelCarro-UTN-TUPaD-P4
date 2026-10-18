# CASO PRÁCTICO — Parte A: Backend con FastAPI

Tomando como base el trabajo práctico de la unidad 6:

---

## a) Entorno virtual y dependencias

```
python -m venv .venv  
source .venv/bin/activate    # macOS/Linux  
.venv\Scripts\activate       # Windows  
pip install -r requirements.txt  
```

---

## b) Models y Schemas

Definir los **models** y **schemas** del módulo **Catálogo de Productos** restantes  
(SVG adjunto al PDF).

---

## c) Campos de auditoría

Agregar al módulo **“Catálogo de productos”** los campos de auditoría:

- created_at  
- updated_at  
- deleted_at  

---

## d) CRUD con arquitectura Models–Schemas–Service–Router

---

## Categorías

| Método | Endpoint            | Body              | Response                     | Query Params                                      |
|--------|---------------------|-------------------|------------------------------|----------------------------------------------------|
| GET    | `/categorias/`      | —                 | CategoriaPaginatedResponse   | offset, limit, nombre, incluir_inactivos           |
| POST   | `/categorias/`      | CategoriaCreate   | CategoriaRead (201)          | —                                                  |
| GET    | `/categorias/{id}`  | —                 | CategoriaRead                | —                                                  |
| PUT    | `/categorias/{id}`  | CategoriaUpdate   | CategoriaRead                | —                                                  |
| DELETE | `/categorias/{id}`  | —                 | 204 No Content               | —                                                  |

---

## Productos

| Método | Endpoint           | Body              | Response                      | Query Params                                      |
|--------|--------------------|-------------------|-------------------------------|----------------------------------------------------|
| GET    | `/productos/`      | —                 | ProductoPaginatedResponse     | offset, limit, nombre, incluir_inactivos           |
| POST   | `/productos/`      | ProductoCreate    | ProductoRead (201)            | —                                                  |
| GET    | `/productos/{id}`  | —                 | ProductoRead                  | —                                                  |
| PUT    | `/productos/{id}`  | ProductoUpdate    | ProductoRead                  | —                                                  |
| DELETE | `/productos/{id}`  | —                 | 204 No Content                | —                                                  |

# Relaciones N:M (solo consulta)

No existen endpoints **POST** ni **DELETE** para gestionar relaciones.  
Las asociaciones se crean o actualizan **únicamente** al crear o editar el producto.

| Método | Endpoint                       | Descripción                    |
|--------|--------------------------------|--------------------------------|
| GET    | `/productos/{id}/categorias`   | Categorías de un producto      |
| GET    | `/categorias/{id}/productos`   | Productos de una categoría     |

# Health

| Método | Endpoint        | Response |
|--------|-----------------|----------|
| GET    | `/health/`      | 200 OK   |
| GET    | `/health/db`    | 200 OK   |

---

# Notas importantes

- Agregar **CORS** para permitir consumo desde el frontend.
- No se debe borrar nada físicamente de la base de datos → **borrado lógico** en todos los modelos.
- Las tablas **Catalog** se cargan desde `seed.py`.  
  **No** deben tener operaciones de escritura (POST/PUT/PATCH).  
  Solo **GET**.

---

# Ejecutar el servidor

```
python -m fastapi dev main.py
```
# 📘 Parte B — Frontend con React + TypeScript (MEJORADO)

---

## g) Páginas (Routing)

La aplicación debe estar organizada en **páginas separadas**.

Crear en `src/pages/`:

- `CategoriasPage.tsx`
- `ProductsPage.tsx`

---

## CategoriasPage

Debe contener **toda la lógica de categorías**:

- useQuery  
- useMutation  
- manejo del modal  

Renderiza:

- CategoriaList  
- CategoriaModal  
- botón **“Nueva categoría”**

---

## ProductsPage

Estructura similar a `CategoriasPage`.

Debe estar preparada para trabajar con productos:

- listado  
- formulario (modal o página)  
- puede reutilizar lógica (recomendado)

---

## h) Navegación

Implementar rutas usando **React Router**.

Instalar:

```
pnpm add react-router-dom
```

### Configuración básica

Definir rutas:

- `/categorias` → CategoriasPage  
- `/productos` → ProductsPage  

### Navbar

Actualizar `Navbar.tsx` para incluir navegación:

- Link a **Categorías**  
- Link a **Productos**

---

## i) App.tsx (cambio clave)

Ahora `App.tsx` **no tiene lógica de negocio**.

Solo debe encargarse de:

- Definir rutas  
- Renderizar el Navbar  
- Mostrar las páginas  

### Comportamiento esperado

- La app inicia en `/categorias`  
- Se puede navegar a `/productos`  
- Cada página maneja su propia lógica  
- No hay lógica mezclada en App (orden profesional)

---

# 📘 Historias de Usuario

Las historias describen el comportamiento esperado desde la perspectiva del usuario.

Cada historia incluye criterios de aceptación verificables.

---

## HU-01 — Listar categorías

**Como** administrador del catálogo,  
**quiero** ver al ingresar la aplicación la lista de todas las categorías,  
**para** tener una visión inmediata del inventario.

### Criterios de aceptación

- Al montar `CategoriasPage` se ejecuta `useQuery` con GET `/categorias`, que responde 200 con la lista.  
- Cada categoría se muestra con nombre y descripción.  
- Si no existen categorías, se muestra un estado vacío comprensible.  
- Si la petición falla, se informa el error con formato `{"detail": "..."}`.

**Canal de verificación:** Frontend (React)

---

## HU-02 — Crear una categoría

**Como** administrador del catálogo,  
**quiero** crear una nueva categoría mediante un formulario en un modal,  
**para** incorporar una clasificación que todavía no existe.

### Criterios de aceptación

- Un botón **“Nueva categoría”** abre el modal con el formulario vacío.  
- El formulario valida nombre obligatorio con `min_length=1` y rechaza solo espacios.  
- Al guardar se envía POST `/categorias`, que responde:
  - **201** si se crea correctamente  
  - **409** si ya existe el nombre  
- Tras una respuesta exitosa:
  - la nueva categoría aparece en la lista **sin recargar la página**  
  - el modal se cierra  

**Canal de verificación:** Frontend (React)

---
