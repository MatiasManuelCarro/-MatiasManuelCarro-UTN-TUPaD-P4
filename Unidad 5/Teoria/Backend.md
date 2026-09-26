# Explicación paso a paso del Service Categoria

A continuación se detalla qué hace cada línea del servicio, de forma clara y técnica.

---

## Código del servicio

```python
def crear_categoria(session: Session, data: CategoriaCreate) -> Categoria:
    existe = session.exec(select(Categoria).where(Categoria.codigo == data.codigo)).first()
    if existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe categotia con codigo: {data.codigo}"
        )
    nueva_categoria = Categoria(**data.model_dump())
    session.add(nueva_categoria)
    session.commit()
    session.refresh(nueva_categoria)
    return nueva_categoria
```

---

## Línea por línea

### 1. Definición de la función

```python
def crear_categoria(session: Session, data: CategoriaCreate) -> Categoria:
```

- Define el servicio de alta de categorías.
- Recibe:
  - `session`: conexión activa a PostgreSQL.
  - `data`: datos validados del POST (`CategoriaCreate`).
- Devuelve una instancia persistida de `Categoria`.

---

### 2. Búsqueda de duplicados

```python
existe = session.exec(select(Categoria).where(Categoria.codigo == data.codigo)).first()
```

- `select(Categoria)` arma una consulta SQL para la tabla.
- `.where(Categoria.codigo == data.codigo)` filtra por código.
- `session.exec(```)` ejecuta la consulta.
- `.first()` devuelve:
  - la categoría encontrada, o
  - `None` si no existe.
- Resultado: `existe` indica si el código ya está usado.

---

### 3. Validación de unicidad

```python
if existe:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"Ya existe categotia con codigo: {data.codigo}"
    )
```

- Si `existe` no es `None`, significa que el código está repetido.
- Se lanza una excepción HTTP:
  - `409 CONFLICT`: conflicto por duplicado.
  - Mensaje claro para el cliente.
- La ejecución se detiene y no se crea nada.

---

### 4. Construcción del modelo persistente

```python
nueva_categoria = Categoria(**data.model_dump())
```

- `data.model_dump()` convierte el schema en un diccionario.
- `Categoria(**```)` crea una instancia del modelo de tabla.
- `id` queda en `None`, lo cual es correcto: PostgreSQL la generará automáticamente.

    - Que hace ** - (expandir diccionario como argumentos nombrados).  
    Convierte 
    ```python
    {"codigo": "```", "descripcion": "```", "activo": True}      
    ```
    en Categoria
    ```python
    (codigo="```", descripcion="```", activo=True).
    ```
---

### 5. Agregar a la sesión

```python
session.add(nueva_categoria)
```

- Marca el objeto como pendiente de inserción.
- Todavía no se ejecutó el `INSERT`.

---

### 6. Confirmar la transacción

```python
session.commit()
```

- Ejecuta el `INSERT` en PostgreSQL.
- La fila queda guardada.
- PostgreSQL genera la `id` automáticamente.

---

### 7. Refrescar el objeto

```python
session.refresh(nueva_categoria)
```

- Vuelve a consultar la fila recién insertada.
- Completa campos generados por la base:
  - `id`
  - valores por defecto.
- Ahora `nueva_categoria.id` tiene el valor real.

---

### 8. Devolver la categoría creada

```python
return nueva_categoria
```

- Devuelve el objeto persistido.
- El router lo serializa usando `CategoriaPublic`.

---

## Resumen

- Valida duplicados por código.
- Crea la categoría con datos validados.
- Inserta en PostgreSQL.
- Recupera la `id` generada automáticamente.
- Devuelve la categoría lista para enviar al cliente.

---
---

# Servicio: listar_categorias
Implementación y explicación técnica del servicio encargado de obtener
categorías desde la base de datos con filtros opcionales y paginación.

---

## Código del servicio

```python
def listar_categorias(
    session: Session,
    skip: int = 0,
    limit: int = 10,
    activo: bool | None = None,
) -> list[Categoria]:
    query = select(Categoria)
    if activo is not None:
        query = query.where(Categoria.activo == activo)
    query = query.offset(skip).limit(limit)
    return list(session.exec(query).all())
```

---

## Explicación línea por línea

### 1. Firma de la función

- `session`: conexión activa a PostgreSQL.
- `skip`: cantidad de registros a saltar (paginación).
- `limit`: cantidad máxima de registros a devolver.
- `activo`: filtro opcional; si es `None`, no se aplica ningún filtro.

Todos los parámetros con valor por defecto están correctamente ubicados después de los que no lo tienen, cumpliendo la regla de Python.

---

### 2. Construcción base de la consulta

```python
query = select(Categoria)
```

Se crea una consulta SQL inicial que selecciona todas las filas de la tabla `Categoria`.  
Todavía no tiene filtros ni paginación.

---

### 3. Filtro opcional por estado `activo`

```python
if activo is not None:
    query = query.where(Categoria.activo == activo)
```

- Si `activo` es `True`, se devuelven solo categorías activas.
- Si `activo` es `False`, se devuelven solo categorías inactivas.
- Si `activo` es `None`, no se aplica ningún filtro.

Esto permite que el endpoint soporte consultas como:

- `/categorias?activo=true`
- `/categorias?activo=false`
- `/categorias` (sin filtro)

---

### 4. Paginación

```python
query = query.offset(skip).limit(limit)
```

- `offset(skip)` salta los primeros `skip` registros.
- `limit(limit)` limita la cantidad de resultados devueltos.

Esto permite paginar correctamente los resultados y evita traer demasiados datos en una sola consulta.

---

### 5. Ejecución de la consulta

```python
return list(session.exec(query).all())
```

- `session.exec(query)` ejecuta la consulta en PostgreSQL.
- `.all()` obtiene todos los resultados.
- `list(```)` convierte el resultado en una lista real.

El servicio devuelve una lista de instancias `Categoria` listas para ser serializadas por el router.

---

## Resumen

- Construye la consulta base.
- Aplica filtro opcional por `activo`.
- Aplica paginación con `skip` y `limit`.
- Ejecuta la consulta y devuelve los resultados como lista.
- Implementación limpia, eficiente y totalmente compatible con FastAPI + SQLModel.

---
---

# Servicio: obtener_por_id
Implementación y explicación técnica del servicio encargado de obtener
una categoría por su ID desde la base de datos.

---

## Código del servicio (corregido)

```python
def obtener_por_id(session: Session, categoria_id: int) -> Categoria:
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria no encontrada"
        )
    return categoria
```

---

## Explicación línea por línea

### 1. Firma de la función

- `session`: conexión activa a PostgreSQL.
- `categoria_id`: ID de la categoría a buscar.
- Devuelve una instancia `Categoria` si existe.

---

### 2. Obtener la categoría por ID

```python
categoria = session.get(Categoria, categoria_id)
```

- `session.get(Modelo, id)` es la forma más directa y eficiente de obtener una fila por su primary key.
- Si existe, devuelve una instancia `Categoria`.
- Si no existe, devuelve `None`.

---

### 3. Validación de existencia

```python
if not categoria:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Categoria no encontrada"
    )
```

- Si `categoria` es `None`, significa que no hay ninguna fila con ese ID.
- Se lanza un error HTTP 404.
- El cliente recibe un mensaje claro.

---

### 4. Devolver la categoría encontrada

```python
return categoria
```

- Devuelve la instancia real de `Categoria`.
- El router la serializa usando el `response_model` correspondiente.
- Esto permite que el cliente reciba:
  - `id`
  - `codigo`
  - `descripcion`
  - `activo`

---

## Resumen

- Busca la categoría por ID usando `session.get`.
- Si no existe, devuelve 404.
- Si existe, devuelve la instancia completa.
- La última línea debe ser `return categoria`, no `return Categoria`.

---
---
# Servicio: actualizar_categoria
Implementación y explicación técnica del servicio encargado de actualizar
una categoría existente utilizando un esquema de actualización parcial (`CategoriaUpdate`).

---

## Código del servicio

```python
def actualizar_categoria(session: Session, categoria_id: int, data: CategoriaUpdate) -> Categoria:
    categoria = obtener_por_id(session, categoria_id)
    cambios = data.model_dump(exclude_unset=True)
    categoria.sqlmodel_update(cambios)
    
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria
```

---

## Explicación línea por línea

### 1. Firma de la función

- `session`: conexión activa a PostgreSQL.
- `categoria_id`: ID de la categoría a actualizar.
- `data`: objeto `CategoriaUpdate` con los campos opcionales a modificar.
- Devuelve la categoría actualizada.

---

### 2. Obtener la categoría existente

```python
categoria = obtener_por_id(session, categoria_id)
```

- Reutiliza el servicio `obtener_por_id`.
- Si la categoría no existe, ese servicio ya lanza un `HTTPException 404`.
- Si existe, devuelve la instancia `Categoria` que se va a modificar.

---

### 3. Extraer solo los campos enviados por el cliente

```python
cambios = data.model_dump(exclude_unset=True)
```

- `model_dump(exclude_unset=True)` genera un diccionario **solo con los campos que el cliente envió**.
- Si el cliente no envía un campo, ese campo **no aparece** en el diccionario.
- Ejemplo:
  - Si el cliente manda `{ "descripcion": "Nueva desc" }`
  - Entonces `cambios` será:
    ```
    { "descripcion": "Nueva desc" }
    ```
- Esto permite actualizaciones parciales sin pisar valores existentes.

---

### 4. Aplicar los cambios al modelo persistente

```python
categoria.sqlmodel_update(cambios)
```

- `sqlmodel_update` aplica cada clave del diccionario como atributo del modelo.
- Es equivalente a hacer:
    ```
    categoria.descripcion = cambios["descripcion"]
    ```
pero de forma automática y segura.
- Solo actualiza los campos presentes en `cambios`.

---

### 5. Guardar cambios en la base

```python
session.add(categoria)
session.commit()
```

- `session.add(categoria)` marca la instancia como modificada.
- `session.commit()` ejecuta el `UPDATE` en PostgreSQL.
- Los cambios quedan persistidos.

---

### 6. Refrescar la instancia

```python
session.refresh(categoria)
```

- Vuelve a consultar la fila actualizada.
- Asegura que el objeto `categoria` tenga los valores reales de la base.
- Útil si la base aplica triggers, defaults o transformaciones.

---

### 7. Devolver la categoría actualizada

```python
return categoria
```

- Devuelve la instancia final.
- El router la serializa usando `CategoriaPublic`.

---

## Resumen

- Obtiene la categoría por ID.
- Extrae solo los campos enviados por el cliente.
- Actualiza la instancia sin pisar valores no enviados.
- Persiste los cambios en PostgreSQL.
- Devuelve la categoría actualizada.

Implementación limpia, segura y totalmente compatible con FastAPI + SQLModel.

