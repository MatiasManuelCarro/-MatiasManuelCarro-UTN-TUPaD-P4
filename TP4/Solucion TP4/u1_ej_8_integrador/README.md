## Se cargan los requirements 

```
pip install -r requirements.txt
```
Salida de la instalacion: 

```powershell

Requirement already satisfied: fastapi[standard] in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from -r requirements.txt (line 1)) (0.141.1)
Requirement already satisfied: starlette>=0.46.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi[standard]->-r requirements.txt (line 1)) (1.6.0)
Requirement already satisfied: pydantic>=2.9.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi[standard]->-r requirements.txt (line 1)) (2.13.5)
Requirement already satisfied: typing-extensions>=4.8.0 in c:\users\matias.carro\appdata\roaming\python\python314\site-packages (from fastapi[standard]->-r requirements.txt (line 1)) (4.16.0)
Requirement already satisfied: typing-inspection>=0.4.2 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi[standard]->-r requirements.txt (line 1)) (0.4.4)
Requirement already satisfied: annotated-doc>=0.0.2 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi[standard]->-r requirements.txt (line 1)) (0.0.5)
Requirement already satisfied: fastapi-cli>=0.0.32 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi-cli[standard]>=0.0.32; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (0.0.32)
Requirement already satisfied: fastar>=0.9.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi[standard]->-r requirements.txt (line 1)) (0.12.0)
Requirement already satisfied: httpx<1.0.0,>=0.23.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi[standard]->-r requirements.txt (line 1)) (0.28.1)
Requirement already satisfied: jinja2>=3.1.5 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi[standard]->-r requirements.txt (line 1)) (3.1.6)
Requirement already satisfied: python-multipart>=0.0.18 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi[standard]->-r requirements.txt (line 1)) (0.0.32)
Requirement already satisfied: email-validator>=2.0.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi[standard]->-r requirements.txt (line 1)) (2.3.0)
Requirement already satisfied: uvicorn>=0.12.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from uvicorn[standard]>=0.12.0; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (0.52.4)
Requirement already satisfied: pydantic-settings>=2.0.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi[standard]->-r requirements.txt (line 1)) (2.15.0)
Requirement already satisfied: pydantic-extra-types>=2.0.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi[standard]->-r requirements.txt (line 1)) (2.11.1)
Requirement already satisfied: anyio in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from httpx<1.0.0,>=0.23.0->fastapi[standard]->-r requirements.txt (line 1)) (4.15.1)
Requirement already satisfied: certifi in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from httpx<1.0.0,>=0.23.0->fastapi[standard]->-r requirements.txt (line 1)) (2026.7.22)
Requirement already satisfied: httpcore==1.* in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from httpx<1.0.0,>=0.23.0->fastapi[standard]->-r requirements.txt (line 1)) (1.0.9)
Requirement already satisfied: idna in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from httpx<1.0.0,>=0.23.0->fastapi[standard]->-r requirements.txt (line 1)) (3.19)
Requirement already satisfied: h11>=0.16 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from httpcore==1.*->httpx<1.0.0,>=0.23.0->fastapi[standard]->-r requirements.txt (line 1)) (0.16.0)
Requirement already satisfied: dnspython>=2.0.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from email-validator>=2.0.0->fastapi[standard]->-r requirements.txt (line 1)) (2.8.0)
Requirement already satisfied: typer>=0.16.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi-cli>=0.0.32->fastapi-cli[standard]>=0.0.32; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (0.27.2)
Requirement already satisfied: rich-toolkit>=0.14.8 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi-cli>=0.0.32->fastapi-cli[standard]>=0.0.32; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (0.20.5)
Requirement already satisfied: fastapi-cloud-cli>=0.1.1 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi-cli[standard]>=0.0.32; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (0.25.0)
Requirement already satisfied: rignore>=0.5.1 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi-cloud-cli>=0.1.1->fastapi-cli[standard]>=0.0.32; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (0.8.1)
Requirement already satisfied: sentry-sdk>=2.20.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi-cloud-cli>=0.1.1->fastapi-cli[standard]>=0.0.32; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (2.69.1)
Requirement already satisfied: detect-installer>=0.1.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi-cloud-cli>=0.1.1->fastapi-cli[standard]>=0.0.32; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (0.2.1)
Requirement already satisfied: agent-detector>=1.1.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from fastapi-cloud-cli>=0.1.1->fastapi-cli[standard]>=0.0.32; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (2.0.0)
Requirement already satisfied: MarkupSafe>=2.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from jinja2>=3.1.5->fastapi[standard]->-r requirements.txt (line 1)) (3.0.3)
Requirement already satisfied: annotated-types>=0.6.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from pydantic>=2.9.0->fastapi[standard]->-r requirements.txt (line 1)) (0.8.0)
Requirement already satisfied: pydantic-core==2.46.5 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from pydantic>=2.9.0->fastapi[standard]->-r requirements.txt (line 1)) (2.46.5)
Requirement already satisfied: python-dotenv>=0.21.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from pydantic-settings>=2.0.0->fastapi[standard]->-r requirements.txt (line 1)) (1.2.3)
Requirement already satisfied: click>=8.1.7 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from rich-toolkit>=0.14.8->fastapi-cli>=0.0.32->fastapi-cli[standard]>=0.0.32; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (8.5.0)
Requirement already satisfied: rich>=13.7.1 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from rich-toolkit>=0.14.8->fastapi-cli>=0.0.32->fastapi-cli[standard]>=0.0.32; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (15.0.0)
Requirement already satisfied: markdown-it-py>=2.2.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from rich>=13.7.1->rich-toolkit>=0.14.8->fastapi-cli>=0.0.32->fastapi-cli[standard]>=0.0.32; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (4.2.0)
Requirement already satisfied: pygments<3.0.0,>=2.13.0 in c:\users\matias.carro\appdata\roaming\python\python314\site-packages (from rich>=13.7.1->rich-toolkit>=0.14.8->fastapi-cli>=0.0.32->fastapi-cli[standard]>=0.0.32; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (2.20.0)
Requirement already satisfied: mdurl~=0.1 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from markdown-it-py>=2.2.0->rich>=13.7.1->rich-toolkit>=0.14.8->fastapi-cli>=0.0.32->fastapi-cli[standard]>=0.0.32; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (0.1.2)
Requirement already satisfied: urllib3>=1.26.11 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from sentry-sdk>=2.20.0->fastapi-cloud-cli>=0.1.1->fastapi-cli[standard]>=0.0.32; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (2.7.0)
Requirement already satisfied: shellingham>=1.3.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from typer>=0.16.0->fastapi-cli>=0.0.32->fastapi-cli[standard]>=0.0.32; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (1.5.4)
Requirement already satisfied: colorama in c:\users\matias.carro\appdata\roaming\python\python314\site-packages (from typer>=0.16.0->fastapi-cli>=0.0.32->fastapi-cli[standard]>=0.0.32; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (0.4.6)
Requirement already satisfied: httptools>=0.8.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from uvicorn[standard]>=0.12.0; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (0.8.0)
Requirement already satisfied: pyyaml>=5.1 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from uvicorn[standard]>=0.12.0; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (6.0.3)
Requirement already satisfied: watchfiles>=0.20 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from uvicorn[standard]>=0.12.0; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (1.2.0)
Requirement already satisfied: websockets>=13.0 in c:\users\matias.carro\appdata\local\programs\python\python314\lib\site-packages (from uvicorn[standard]>=0.12.0; extra == "standard"->fastapi[standard]->-r requirements.txt (line 1)) (17.1)
```

## Se carga el entorno virtual

```
fastapi dev app/main.py
```

Salida de la consola

```
 ⚡️ Starting FastAPI in development mode
 
 🐍 Using import string: app.main:app
 
 🌐 Server started at http://127.0.0.1:8000
    Documentation at http://127.0.0.1:8000/docs
 
  Logs:

 ▕  Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
 ▕  Started reloader process [32032] using WatchFiles
 ▕  Started server process [11604]
 ▕  Waiting for application startup.
 ▕  Application startup complete.
 ▕  127.0.0.1:55697 - "GET /docs HTTP/1.1" 200

```