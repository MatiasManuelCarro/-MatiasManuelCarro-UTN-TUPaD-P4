# API Consultorio — Gestión de Turnos

CRUD persistente sobre PostgreSQL con FastAPI + SQLModel, siguiendo la
arquitectura en capas de la unidad: `Router → Service → Schema → Model`.

## Dominio

Dos entidades relacionadas uno-a-muchos: un **Paciente** puede tener muchos
**Turnos**.

- `Paciente`: guarda un dato interno (`obra_social`) que jamás se devuelve
  al cliente, y tiene baja lógica (`activo`) en lugar de borrado físico.
- `Turno`: pertenece a un paciente (`paciente_id` como foreign key), y tiene
  un ciclo de estados: `pendiente → confirmado → atendido`, o
  `pendiente/confirmado → cancelado`.

## Estructura del proyecto

```
gestor_turnos_consultorio/
├── main.py            # instancia FastAPI, incluye los routers
├── database.py        # engine, Session por request, create_db_and_tables
├── requirements.txt
├── .env.example
├── test_requests/      # payloads de prueba + archivo .http
└── app/
    ├── models/         # tablas persistentes (SQLModel, table=True)
    ├── schemas/        # contratos de entrada/salida (Create/Public/Update)
    ├── service/        # lógica de negocio y transacciones
    └── routers/        # endpoints HTTP
```

## Puesta en marcha

1. Crear la base en PostgreSQL:
   ```sql
   CREATE DATABASE turnos_db;
   ```
2. Copiar `.env.example` a `.env` y ajustar la cadena de conexión, o exportar
   `DATABASE_URL` directamente.
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Levantar el servidor:
   ```bash
   uvicorn main:app --reload
   ```
5. Abrir `http://localhost:8000/docs` (Swagger UI) o `http://localhost:8000/redoc`.

## Probar los endpoints

En `test_requests/` hay JSONs de ejemplo para cada operación de creación y
actualización, y un archivo `requests.http` (compatible con la extensión
REST Client de VS Code) con la secuencia completa lista para ejecutar. Los
mismos JSON sirven como body en Postman o Swagger UI.

## Endpoints principales

| Método | Ruta                          | Descripción                              |
|--------|-------------------------------|-------------------------------------------|
| POST   | `/pacientes/`                 | Crear paciente (409 si el DNI ya existe) |
| GET    | `/pacientes/`                 | Listar pacientes (filtro `activo`)       |
| GET    | `/pacientes/{id}`             | Obtener paciente con sus turnos          |
| PATCH  | `/pacientes/{id}`              | Actualizar datos parciales               |
| PATCH  | `/pacientes/{id}/desactivar`  | Baja lógica (409 si ya estaba inactivo)  |
| POST   | `/turnos/`                    | Crear turno (valida paciente, fecha, solapamiento) |
| GET    | `/turnos/`                    | Listar turnos (filtros: estado, paciente_id, fecha) |
| GET    | `/turnos/{id}`                | Obtener un turno                         |
| PATCH  | `/turnos/{id}`                 | Reprogramar (solo si no está finalizado) |
| PATCH  | `/turnos/{id}/confirmar`      | pendiente → confirmado                   |
| PATCH  | `/turnos/{id}/cancelar`       | Cancela el turno (409 si ya estaba finalizado) |

## Reglas de negocio implementadas

- DNI de paciente único → `409 Conflict` si se repite.
- No se pueden crear turnos para un paciente inactivo, ni en una fecha
  pasada (`400 Bad Request`).
- No se permite superponer turnos del mismo profesional en el mismo
  horario (`409 Conflict`).
- Un turno cancelado o atendido no se puede modificar ni volver a cancelar.
- Los modelos de entrada y salida están siempre separados: nunca se expone
  el modelo de base de datos directamente al cliente.
