# FastApi 

## Activar entorno

En directorio: fastapi_backend
```powershell
source .venv/bin/activate
```

## Ir al directorio del ejercicio

Ej: (.venv) ➜ fastapi_backend cd u_01/u1_ej4/

## Ejecutar servidor de desarrollo con Endpints

(.venv) ➜ u1_ej4 

```powershell
python -m fastapi dev ej_4_1.py
```

---

## 📌 Guía de Instalación y Ejecución de la API

Este documento detalla el paso a paso para configurar el entorno de desarrollo local y ejecutar nuestra API construida con **FastAPI**.

### Paso 1: Crear el Entorno Virtual (Virtual Environment)
Es una buena práctica en Python aislar las librerías de cada proyecto para evitar conflictos de versiones. Vamos a crear un entorno virtual llamado `.venv` dentro de la carpeta de nuestro proyecto.

Abre una terminal en la raíz del proyecto y ejecuta:

```powershell
python -m venv .venv
```
*(Nota: Si usas una versión específica de Python, puedes usar algo como `python3 -m venv .venv` o la ruta completa al ejecutable).*

### Paso 2: Activar el Entorno Virtual
Una vez creado, debemos "encenderlo" para que todo lo que instalemos de ahora en adelante quede guardado allí adentro y no en el sistema global.

En tu consola de PowerShell, ejecuta:

```powershell
.\.venv\Scripts\Activate.ps1
```
*(Sabrás que funcionó porque en tu terminal aparecerá un `(.venv)` al principio de la línea de comandos. Si PowerShell te da un error de permisos de ejecución de scripts, ejecuta primero `Set-ExecutionPolicy Unrestricted -Scope CurrentUser`).*

> **Nota para salir:** Cuando termines de trabajar en el proyecto y quieras "apagar" o salir del entorno virtual, simplemente escribe el comando `deactivate` en la consola y presiona Enter. El prefijo `(.venv)` desaparecerá, indicando que has vuelto al entorno normal de tu computadora.

### Paso 3: Actualizar pip
Antes de instalar cualquier librería, es muy recomendable tener `pip` (el gestor de paquetes de Python) actualizado a su última versión. Esto asegura que la instalación de nuestras herramientas sea rápida y sin errores de compatibilidad.

Con el entorno virtual activado, ejecuta el siguiente comando en Windows:

```powershell
python -m pip install --upgrade pip
```

### Paso 4: Instalar Paquetes y Dependencias
Para mantener el proyecto organizado y asegurar que todos los miembros del equipo tengan las mismas dependencias, utilizaremos un archivo de texto para gestionarlas.

1. **Crear el archivo:** En la raíz del proyecto, crea un archivo llamado `requirements.txt`.
2. **Agregar los paquetes:** Abre el archivo y escribe los nombres de las librerías que necesitamos (una por línea). Por ejemplo:
   ```text
   fastapi[standard]
   uvicorn
   ```
3. **Instalar dependencias:** En la terminal (con el entorno virtual activado), ejecuta el siguiente comando para que Python lea el archivo e instale todo automáticamente:
   ```powershell
   pip install -r requirements.txt
   ```
4. **Verificar la instalación:** Para comprobar qué librerías se instalaron finalmente en tu entorno virtual, ejecuta:
   ```powershell
   python -m pip list
   ```
   *(Nota: Dependiendo de tu instalación de Python, el comando podría ser `python3 -m pip list`).*

   *Ejemplo de salida*

   ```powerhsell
    Package              Version
    -------------------- ---------
    agent-detector       2.0.0
    annotated-doc        0.0.5
    annotated-types      0.8.0
    anyio                4.15.1
    certifi              2026.7.22
    click                8.5.0
    colorama             0.4.6
    detect-installer     0.2.1
    dnspython            2.8.0
    email-validator      2.3.0
    fastapi              0.141.1
    fastapi-cli          0.0.32
    fastapi-cloud-cli    0.25.0
    fastar               0.12.0
    h11                  0.16.0
    httpcore             1.0.9
    httptools            0.8.0
    httpx                0.28.1
    idna                 3.19
    Jinja2               3.1.6
    markdown-it-py       4.2.0
    MarkupSafe           3.0.3
    mdurl                0.1.2
    pip                  26.2.1
    pydantic             2.13.5
    pydantic_core        2.46.5
    pydantic-extra-types 2.11.1
    pydantic-settings    2.15.0
    Pygments             2.21.0
    python-dotenv        1.2.3
    python-multipart     0.0.32
    PyYAML               6.0.3
    rich                 15.0.0
    rich-toolkit         0.20.4
    rignore              0.8.1
    sentry-sdk           2.68.1
    shellingham          1.5.4
    starlette            1.6.0
    typer                0.27.2
    typing_extensions    4.16.0
    typing-inspection    0.4.4
    urllib3              2.7.0
    uvicorn              0.52.4
    watchfiles           1.2.0
    websockets           17.1
    ```
### Paso 5: Primer Ejemplo (Hola Mundo)
Para comprobar que todo funciona correctamente, vamos a crear nuestra primera ruta básica en la API.

1. En la raíz del proyecto, crea un archivo llamado `main.py`.
2. Abre el archivo y pega el siguiente código:

```python
from fastapi import FastAPI

# Inicializamos la aplicación
app = FastAPI()

# Definimos la ruta raíz (GET)
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### Paso 6: Ejecutar el Servidor
Para encender la API, utilizaremos la CLI (Interfaz de Línea de Comandos) integrada de FastAPI. Este comando levanta el servidor en modo desarrollo, lo que significa que detectará automáticamente cualquier cambio que guardes en el código y se reiniciará solo.

> **⚠️ Nota importante:** Asegúrate de que tu terminal esté posicionada en el directorio correspondiente (la misma carpeta donde creaste el archivo `main.py`). Si estás en otra carpeta, usa el comando `cd` (ej: `cd ruta\de\tu\proyecto`) para navegar hasta allí antes de ejecutar el servidor.

En tu terminal (con el entorno virtual activado), ejecuta:

```powershell
python -m fastapi dev main.py
```

### Paso 7: Probar la API desde el Navegador
Una vez que la consola indique que el servidor está corriendo, puedes probarlo de dos formas:

1. **Ver la respuesta cruda:** Abre tu navegador y entra a `http://127.0.0.1:8000`. Verás el mensaje `{"message": "Hello World"}`.
2. **Ver la Documentación Interactiva (Swagger):** Entra a `http://127.0.0.1:8000/docs`. Aquí verás una interfaz gráfica generada automáticamente donde podrás probar todos los métodos y rutas que vayamos creando.

> **Para detener el servidor:** Haz clic en la terminal donde está corriendo y presiona `CTRL + C`.

### Paso 8: Probar la API (HTTP Test)
También puedes probar tu API simulando peticiones HTTP (Send Request). Tienes dos opciones para hacerlo:

**Opción A: Usando el editor de código (REST Client / Archivos .http)**
Si utilizas editores como VS Code (con la extensión REST Client) o PyCharm, puedes crear un archivo temporal con extensión `.http` o `.rest` y pegar la petición cruda:
```http
GET [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
Accept: application/json
```

**Opción B: Usando curl desde la consola**
Abre una **nueva pestaña o ventana** en tu terminal (para no apagar el servidor que ya está corriendo) y ejecuta:
```bash
curl -X 'GET' \
  '[http://127.0.0.1:8000/](http://127.0.0.1:8000/)' \
  -H 'accept: application/json'
```

**Salida de ejemplo:**
Cualquiera sea el método que elijas, el servidor procesará la petición y devolverá los encabezados HTTP (mostrando un código `200 OK` de éxito) junto con el cuerpo de la respuesta en formato JSON:

```http
HTTP/1.1 200 OK
date: Mon, 07 Sep 2026 16:29:35 GMT
server: uvicorn
content-length: 25
content-type: application/json
connection: close

{
  "message": "Hello World"
}
```

---
# Actividad 2 

## 🔗 Conceptos Clave: URLs y Parámetros

### Anatomía de una URL y Recursos
Antes de agregar más rutas, es importante entender cómo se estructuran las direcciones a las que hacemos peticiones en una API REST.

Una **URL** (Uniform Resource Locator) es la "dirección" que indica cómo (mediante un protocolo) y dónde (en qué host) localizar un recurso específico.

La estructura general es:
`{protocolo}://{host}[:puerto]/{ruta}?{query}`

**Ejemplo completo:**
`http://127.0.0.1:8000/items/3?completed=false&limit=20`

*   **Recurso:** Es cualquier cosa identificable por una URL (por ejemplo: un usuario específico, un ítem en un carrito, un archivo de texto).
*   **Representación:** Es el formato en que el servidor decide entregar ese recurso: JSON (lo más común en APIs), HTML, una imagen (PNG/JPG), un video (MP4), un documento PDF, etc.

### Parámetros de Ruta y Orden de Ejecución

**1. Variables Dinámicas (Path Parameters)**
En FastAPI, puedes capturar valores directamente desde la URL utilizando llaves `{}`. Por ejemplo, en la ruta `/items/{user_id}`, el framework tomará el valor que el usuario escriba en esa posición y lo inyectará en la función como la variable `user_id`.

**2. La Regla del Orden (De arriba hacia abajo)**
FastAPI evalúa las rutas en el código línea por línea. En cuanto encuentra la primera coincidencia con la URL solicitada, la ejecuta y deja de buscar. Por este motivo, **las rutas estáticas siempre deben definirse antes que las dinámicas**.

**Ejemplo Práctico:**

```python
# ⚠️ IMPORTANTE: El orden de las rutas importa en FastAPI

# 1. Ruta estática (Debe ir primero)
@app.get("/user/me")
async def read_user_me():
    return {"user": "current"}

# 2. Ruta dinámica (Debe ir después)
@app.get("/user/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```

2. **Prueba el resultado:**
   * Si vas a `http://127.0.0.1:8000/items/matias`, la ruta dinámica lo atrapa y devuelve `{"user_id": "matias"}`.
   * Si vas a `http://127.0.0.1:8000/items/me`, la ruta estática lo atrapa primero y devuelve `{"user": "current"}`.

> **¿Qué pasa si las invertimos?** Si la ruta `/{user_id}` estuviera arriba, al pedir `/items/me`, FastAPI pensaría que la palabra "me" es un ID de usuario y nunca llegaría a ejecutar la función `read_user_me`.

### Parámetros de Ruta con Validación de Tipos (Type Hints)
Hasta ahora, nuestros parámetros de ruta recibían cualquier cosa como texto (String). Pero, ¿qué pasa si queremos que un ID sea estrictamente un número entero? 

En FastAPI, usamos los **Type Hints** de Python para definir el tipo de dato.

1. Modifica tu archivo `main.py` con este código:

```python
from fastapi import FastAPI

app = FastAPI()

# Le indicamos a Python que item_id DEBE ser un entero (int)
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
```

**¿Qué magia hace FastAPI por detrás cuando agregamos `: int`?**
* **Conversión automática (Parsing):** Aunque todo lo que viaja por la URL es texto, FastAPI agarra el `"22"` de la URL y lo convierte automáticamente en el número entero `22` dentro de Python.
* **Validación automática:** Si un usuario intenta enviar texto en lugar de un número, FastAPI bloqueará la petición antes de que llegue a tu función y le devolverá un error claro, evitando que tu código se rompa.

**Prueba en tu archivo `.http` (o REST Client):**

Copia y ejecuta estas dos peticiones para ver la diferencia:

```http
### 1. Prueba Exitosa (Enviando un número)
GET [http://127.0.0.1:8000/items/22](http://127.0.0.1:8000/items/22)
Accept: application/json

### 2. Prueba Fallida (Enviando texto - FastAPI lanza un error 422)
GET [http://127.0.0.1:8000/items/matias](http://127.0.0.1:8000/items/matias)
Accept: application/json
```

Si ejecutas la segunda prueba, verás que la API te responde automáticamente con un mensaje detallado explicando que el valor no es un entero válido (Unprocessable Entity). ¡Todo esto sin que nosotros hayamos escrito ni un solo `if`!

### Valores Predefinidos en Rutas (Enum)
A veces no solo queremos validar el tipo de dato (que sea texto o número), sino que queremos **restringir las opciones** a una lista específica permitida. Para esto, Python nos ofrece la clase `Enum`.

1. Abre `main.py`, importa la librería `Enum` en la parte superior y agrega este código:

```python
from enum import Enum
from fastapi import FastAPI

app = FastAPI()

# 1. Creamos una clase que hereda de str y de Enum
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# 2. Usamos nuestra clase como Type Hint
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    # FastAPI ya validó que model_name solo puede ser uno de los 3 permitidos
    return {"model_name": model_name}
```

**¿Por qué esto es tan útil?**
* **Validación estricta:** Si el usuario escribe `/models/alexnet`, la API responde con éxito. Si inventa algo como `/models/mi_modelo`, FastAPI lo rechaza automáticamente con un error 422.
* **Documentación Automática (Swagger):** Si entras a `http://127.0.0.1:8000/docs`, verás que FastAPI leyó tu `Enum` y convirtió ese campo de texto en un **menú desplegable**, haciendo que la API sea facilísima de usar para otros desarrolladores.

**Prueba en tu archivo `.http`:**

```http
### Prueba Exitosa (Opción permitida)
GET [http://127.0.0.1:8000/models/alexnet](http://127.0.0.1:8000/models/alexnet)
Accept: application/json

### Prueba Fallida (Opción NO permitida - FastAPI la rechaza)
GET [http://127.0.0.1:8000/models/supernet](http://127.0.0.1:8000/models/supernet)
Accept: application/json
```