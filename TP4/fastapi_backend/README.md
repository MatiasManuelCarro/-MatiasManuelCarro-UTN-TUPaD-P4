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
   fastapi
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

### Paso 9: Anatomía de una URL y Recursos
Antes de agregar más rutas, es importante entender cómo se estructuran las direcciones a las que hacemos peticiones en una API REST.

Una **URL** (Uniform Resource Locator) es la "dirección" que indica cómo (mediante un protocolo) y dónde (en qué host) localizar un recurso específico.

La estructura general es:
`{protocolo}://{host}[:puerto]/{ruta}?{query}`

**Ejemplo completo:**
`http://127.0.0.1:8000/items/3?completed=false&limit=20`

*   **Recurso:** Es cualquier cosa identificable por una URL (por ejemplo: un usuario específico, un ítem en un carrito, un archivo de texto).
*   **Representación:** Es el formato en que el servidor decide entregar ese recurso: JSON (lo más común en APIs), HTML, una imagen (PNG/JPG), un video (MP4), un documento PDF, etc.