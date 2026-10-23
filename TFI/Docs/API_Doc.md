# API REST - Sistema de Gestión 107

## 1. Descripción

El backend del Sistema de Gestión 107 expone una API REST para la gestión de:

- Autenticación
- Usuarios
- Categorías
- Insumos
- Ambulancias
- Turnos
- Control de insumos
- Resumen operativo

La API utiliza JSON para el intercambio de información y define un esquema de autenticación mediante Bearer Token JWT.

---

## 2. URL base

En entorno de desarrollo:

```text
http://localhost:8080/api
```

Los endpoints de la aplicación utilizan la versión `/v1`.

Por lo tanto, la URL base recomendada para el frontend es:

```text
http://localhost:8080/api/v1
```

Ejemplo:

```text
GET http://localhost:8080/api/v1/insumos
```

---

## 3. Documentación OpenAPI

### Swagger UI

```text
http://localhost:8080/api/swagger-ui/index.html
```

### OpenAPI JSON

```text
http://localhost:8080/api/v3/api-docs
```

### OpenAPI YAML

```text
http://localhost:8080/api/v3/api-docs.yaml
```

---

# 4. Autenticación

La API define autenticación HTTP Bearer utilizando JWT.

```http
Authorization: Bearer <token>
```

## POST `/v1/auth/login`

Autentica un usuario.

### Request

Schema: `LoginRequestDTO`

```json
{
  "mail": "usuario@email.com",
  "clave": "password"
}
```

| Campo | Tipo | Obligatorio | Restricciones |
|---|---|---|---|
| `mail` | string | Sí | Formato email |
| `clave` | string | Sí | Mínimo 6 caracteres |

### Response

Schema: `LoginDTO`

```json
{
  "access_token": "token",
  "expires_in": 3600000,
  "token_type": "Bearer",
  "scope": "string"
}
```

---

# 5. Usuarios

## Endpoints

| Método | Endpoint | Operación |
|---|---|---|
| GET | `/v1/usuarios` | Listar usuarios |
| GET | `/v1/usuarios/{id}` | Obtener usuario por ID |
| POST | `/v1/usuarios` | Crear usuario |
| PUT | `/v1/usuarios/{id}` | Actualizar usuario |
| DELETE | `/v1/usuarios/{id}` | Eliminar usuario |

## UsuarioDTO

```json
{
  "id": 1,
  "nombre": "string",
  "dni": "string",
  "email": "string",
  "rol": "ADMINISTRADOR",
  "activo": true
}
```

## UsuarioRequestDTO

Utilizado por las operaciones de creación y actualización.

```json
{
  "nombre": "string",
  "dni": "string",
  "email": "usuario@email.com",
  "rol": "ENFERMERO",
  "clave": "string",
  "activo": true
}
```

### RolUsuario

Valores posibles:

```text
ADMINISTRADOR
ENFERMERO
```

---

# 6. Categorías

## Endpoints

| Método | Endpoint | Operación |
|---|---|---|
| GET | `/v1/categorias` | Listar categorías |
| GET | `/v1/categorias/{id}` | Obtener categoría por ID |
| POST | `/v1/categorias` | Crear categoría |
| PUT | `/v1/categorias/{id}` | Actualizar categoría |
| DELETE | `/v1/categorias/{id}` | Eliminar categoría |

## CategoriaInsumoDTO

```json
{
  "id": 1,
  "nombre": "FARMACOLOGICOS",
  "color": "#FF0000"
}
```

## CategoriaInsumoRequestDTO

```json
{
  "nombre": "FARMACOLOGICOS",
  "color": "#FF0000"
}
```

---

# 7. Insumos

## Endpoints

| Método | Endpoint | Operación |
|---|---|---|
| GET | `/v1/insumos` | Listar todos los insumos |
| GET | `/v1/insumos/{id}` | Obtener insumo por ID |
| POST | `/v1/insumos` | Crear insumo |
| PUT | `/v1/insumos/{id}` | Actualizar insumo |
| DELETE | `/v1/insumos/{id}` | Eliminar insumo |
| GET | `/v1/insumos/criticos` | Listar insumos críticos |
| GET | `/v1/insumos/categoria/{categoriaId}` | Listar insumos por categoría |

## InsumoDTO

```json
{
  "id": 1,
  "nombre": "Adrenalina 1mg",
  "categoria": "FARMACOLOGICOS",
  "puntoControl": 20,
  "esCritico": true
}
```

## InsumoRequestDTO

```json
{
  "nombre": "Adrenalina 1mg",
  "categoriaId": 1,
  "puntoControl": 20,
  "critico": true
}
```

| Campo | Tipo | Descripción |
|---|---|---|
| `nombre` | string | Nombre del insumo |
| `categoriaId` | integer | ID de la categoría |
| `puntoControl` | integer | Cantidad de referencia |
| `critico` | boolean | Indica si el insumo es crítico |

---

# 8. Ambulancias

## Endpoints

| Método | Endpoint | Operación |
|---|---|---|
| GET | `/v1/ambulancias` | Listar ambulancias |
| GET | `/v1/ambulancias/{id}` | Obtener ambulancia por ID |
| POST | `/v1/ambulancias` | Crear ambulancia |
| PUT | `/v1/ambulancias/{id}` | Actualizar ambulancia |
| DELETE | `/v1/ambulancias/{id}` | Eliminar ambulancia |

## AmbulanciaDTO

```json
{
  "id": 1,
  "patente": "AA123BB"
}
```

## AmbulanciaRequestDTO

```json
{
  "patente": "AA123BB",
  "disponible": true,
  "insumos": [
    1,
    2,
    3
  ]
}
```

El campo `insumos` contiene un conjunto de IDs de insumos asociados a la ambulancia.

---

# 9. Turnos

## Endpoints

| Método | Endpoint | Operación |
|---|---|---|
| GET | `/v1/turnos` | Listar turnos |
| GET | `/v1/turnos/{id}` | Obtener turno por ID |
| POST | `/v1/turnos` | Crear turno |
| PUT | `/v1/turnos/{id}` | Modificar turno |
| POST | `/v1/turnos/{id}/cancelar` | Cancelar turno |
| POST | `/v1/turnos/ingreso` | Registrar ingreso |
| POST | `/v1/turnos/egreso` | Registrar egreso |
| GET | `/v1/turnos/activos` | Obtener turnos activos |
| GET | `/v1/turnos/enfermero/{enfermeroId}` | Obtener turnos de un enfermero |
| GET | `/v1/turnos/resumen` | Obtener resumen operativo |

---

## TurnoRequestDTO

```json
{
  "fecha": "2026-10-23",
  "horario": "MANIANA",
  "adminId": 1,
  "enfermeroId": 2,
  "ambulanciaId": 1,
  "nombreChofer": "string",
  "nombreMedico": "string"
}
```

## HorarioTurno

Valores posibles:

```text
MANIANA
TARDE
NOCHE
```

---

## TurnoDTO

```json
{
  "id": 1,
  "fecha": "2026-10-23",
  "horario": "MANIANA",
  "estado": "PROGRAMADO",
  "admin": {
    "id": 1,
    "email": "admin@email.com"
  },
  "enfermero": {
    "id": 2,
    "email": "enfermero@email.com"
  },
  "medico": "string",
  "chofer": "string",
  "ambulancia": {
    "id": 1,
    "patente": "AA123BB"
  },
  "observacionesIngreso": "string",
  "observacionesEgreso": "string",
  "controlInsumos": []
}
```

## EstadoTurno

Valores posibles:

```text
PROGRAMADO
EN_CURSO
FINALIZADO
CANCELADO
```

---

# 10. Cancelación de turno

## POST `/v1/turnos/{id}/cancelar`

Cancela el turno identificado por `{id}`.

### CancelarTurnoDTO

```json
{
  "observaciones": "Motivo u observaciones de la cancelación"
}
```

### Response

```text
TurnoDTO
```

---

# 11. Control de ingreso

## POST `/v1/turnos/ingreso`

Registra el control de insumos correspondiente al ingreso del turno.

### Request

Schema: `IngresoEgresoDTO`

```json
{
  "turnoId": 1,
  "insumos": [
    {
      "id": 1,
      "cantidad": 10,
      "cantidadRestockeo": 0
    }
  ],
  "observaciones": "string"
}
```

---

# 12. Control de egreso

## POST `/v1/turnos/egreso`

Registra el control de insumos correspondiente al egreso del turno.

### Request

Schema: `IngresoEgresoDTO`

```json
{
  "turnoId": 1,
  "insumos": [
    {
      "id": 1,
      "cantidad": 8,
      "cantidadRestockeo": 0
    }
  ],
  "observaciones": "string"
}
```

---

# 13. ControlInsumoRequestDTO

```json
{
  "id": 1,
  "cantidad": 10,
  "cantidadRestockeo": 0
}
```

| Campo | Tipo |
|---|---|
| `id` | integer |
| `cantidad` | integer |
| `cantidadRestockeo` | integer |

---

# 14. ControlInsumoDTO

```json
{
  "nombre": "Adrenalina 1mg",
  "categoria": "FARMACOLOGICOS",
  "esCritico": true,
  "cantidadIngreso": 20,
  "cantidadEgreso": 18,
  "ingresoFaltante": 0,
  "cantidadUsada": 2,
  "cantidadRestockeo": 0
}
```

---

# 15. Resumen operativo

## GET `/v1/turnos/resumen`

Devuelve un `ResumenOperativoDTO`.

```json
{
  "turnosActivos": 0,
  "ambulanciasDisponibles": 0,
  "ambulanciasTotales": 0,
  "alertas": 0,
  "turnosConInconsistencias": [],
  "listaAmbulancias": []
}
```

### Campos

| Campo | Tipo |
|---|---|
| `turnosActivos` | integer |
| `ambulanciasDisponibles` | integer |
| `ambulanciasTotales` | integer |
| `alertas` | integer |
| `turnosConInconsistencias` | `TurnoDTO[]` |
| `listaAmbulancias` | `AmbulanciaDTO[]` |

---

# 16. Enumeraciones

## RolUsuario

```text
ADMINISTRADOR
ENFERMERO
```

## HorarioTurno

```text
MANIANA
TARDE
NOCHE
```

## EstadoTurno

```text
PROGRAMADO
EN_CURSO
FINALIZADO
CANCELADO
```

---

# 17. Comunicación con el frontend

El frontend consume la API REST mediante HTTP/JSON.

```text
React + TypeScript
        |
        | HTTP / JSON
        v
Spring Boot REST API
        |
        v
Service
        |
        v
Repository / JPA
        |
        v
Base de datos
```

Durante el desarrollo puede utilizarse H2 como base de datos.

El frontend no accede directamente a H2 ni a MySQL. La comunicación se realiza exclusivamente con los endpoints REST del backend.

Mientras el contrato de la API REST se mantenga, el cambio de base de datos del backend no afecta al consumo de la API desde el frontend.

---

# 18. Configuración del frontend

URL base de desarrollo:

```text
http://localhost:8080/api/v1
```

Se recomienda definirla mediante una variable de entorno de Vite:

```env
VITE_API_URL=http://localhost:8080/api/v1
```

Acceso desde TypeScript:

```ts
const API_URL = import.meta.env.VITE_API_URL;
```

---

# 19. Organización sugerida del frontend

```text
src/
├── components/
├── pages/
├── hooks/
├── services/
│   ├── authService.ts
│   ├── usuarioService.ts
│   ├── categoriaService.ts
│   ├── insumoService.ts
│   ├── ambulanciaService.ts
│   └── turnoService.ts
├── types/
│   ├── auth.ts
│   ├── usuario.ts
│   ├── categoria.ts
│   ├── insumo.ts
│   ├── ambulancia.ts
│   └── turno.ts
└── ...
```

---

# 20. Referencia del contrato

La especificación OpenAPI generada por el backend constituye la referencia del contrato entre backend y frontend.

Puede obtenerse desde:

```text
http://localhost:8080/api/v3/api-docs
```

Contiene:

- endpoints;
- métodos HTTP;
- parámetros;
- request bodies;
- response bodies;
- DTOs;
- tipos;
- enums;
- configuración de seguridad.

Cuando se modifique el contrato del backend, se recomienda volver a exportar `api-docs.json` y revisar esta documentación para mantener sincronizada la integración con el frontend.