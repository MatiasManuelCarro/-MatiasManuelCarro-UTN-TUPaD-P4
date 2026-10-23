# Plan de Desarrollo del Frontend
## Sistema de Gestión y Trazabilidad 107

## 1. Objetivo

Este documento define el orden recomendado para desarrollar el frontend del Sistema de Gestión 107.

El frontend utiliza:

- React
- TypeScript
- Vite
- API REST desarrollada con Spring Boot

La arquitectura definida para el proyecto establece que el frontend debe consumir el backend mediante HTTP/JSON y separar las responsabilidades entre páginas, componentes, servicios y lógica reutilizable.

El objetivo del orden propuesto es desarrollar primero las funcionalidades que funcionan como dependencia de otros módulos y posteriormente construir los procesos operativos.

---

# 2. Flujo funcional general

El sistema puede entenderse mediante el siguiente flujo:

```text
Autenticación
      ↓
Usuarios
      ↓
Categorías
      ↓
Insumos
      ↓
Ambulancias
      ↓
Turnos
      ↓
Control operativo del enfermero
      ↓
Historial
      ↓
Dashboard
```

No todas estas relaciones representan dependencias técnicas estrictas.

El orden se propone principalmente para evitar desarrollar una pantalla que necesite información de módulos todavía no implementados.

Por ejemplo:

```text
Categoría
    ↓
Insumo
    ↓
Ambulancia
    ↓
Turno
    ↓
Control de insumos
```

---

# 3. Estructura recomendada del frontend

La arquitectura definida para el proyecto contempla:

```text
src/
├── components/
├── hooks/
├── interfaces/
├── pages/
├── services/
├── assets/
├── App.tsx
└── main.tsx
```

Responsabilidades recomendadas:

```text
interfaces/
    Tipos TypeScript correspondientes a DTOs del backend.

services/
    Comunicación HTTP con Spring Boot.

hooks/
    Lógica reutilizable relacionada con estado y obtención de datos.

components/
    Componentes reutilizables de interfaz.

pages/
    Pantallas completas de la aplicación.
```

Una página no debería contener directamente toda la lógica HTTP si esa operación puede encapsularse en un servicio.

Ejemplo:

```text
AdminAmbulancias.tsx
        ↓
ambulancias.ts
        ↓
API REST
        ↓
Spring Boot
```

---

# 4. Etapa 0: infraestructura del frontend

## Objetivo

Antes de desarrollar los módulos funcionales conviene estabilizar la comunicación con el backend.

### Crear

```text
src/services/api.ts
```

Ejemplo:

```ts
export const API_URL = "http://localhost:8080/api/v1";
```

Posteriormente puede trasladarse a una variable de entorno:

```env
VITE_API_URL=http://localhost:8080/api/v1
```

Y utilizarse como:

```ts
export const API_URL = import.meta.env.VITE_API_URL;
```

## Recomendaciones

Todas las llamadas HTTP deben utilizar esta URL base.

Evitar:

```ts
fetch("http://localhost:8080/api/v1/usuarios");
```

Preferir:

```ts
fetch(`${API_URL}/usuarios`);
```

También se recomienda centralizar el manejo de respuestas HTTP para:

- detectar `res.ok`;
- procesar errores del backend;
- procesar respuestas JSON;
- soportar respuestas `204 No Content`;
- incorporar posteriormente JWT sin duplicar código.

---

# 5. Etapa 1: Categorías

## Motivo para desarrollar este módulo primero

Los insumos dependen de una categoría.

Por lo tanto:

```text
Categorías
    ↓
Insumos
```

No conviene terminar el ABM de insumos antes de poder consultar las categorías existentes.

## Página

```text
AdminCategorias.tsx
```

Actualmente esta página debería incorporarse al frontend si aún no existe.

## Interface

```text
Categoria.ts
```

## Servicio

```text
categorias.ts
```

## Endpoints

### Listar

```http
GET /v1/categorias
```

### Obtener

```http
GET /v1/categorias/{id}
```

### Crear

```http
POST /v1/categorias
```

Body:

```json
{
  "nombre": "FARMACOLOGICOS",
  "color": "#FF0000"
}
```

### Modificar

```http
PUT /v1/categorias/{id}
```

### Eliminar

```http
DELETE /v1/categorias/{id}
```

## Consideraciones

Una categoría posee:

```text
id
nombre
color
```

El color forma parte del modelo y debería aprovecharse visualmente en el frontend.

La documentación del sistema establece además que el color debe acompañarse con texto y no utilizarse como único mecanismo de identificación.

---

# 6. Etapa 2: Insumos

## Dependencia

```text
Categoría
    ↓
Insumo
```

Cada insumo pertenece a una categoría.

## Página

```text
AdminInsumos.tsx
```

## Interface

```text
Insumo.ts
```

Conviene separar el objeto recibido del objeto enviado:

```ts
export interface Insumo {
  id: number;
  nombre: string;
  categoria: string;
  puntoControl: number;
  esCritico: boolean;
}
```

Y:

```ts
export interface InsumoRequest {
  nombre: string;
  categoriaId: number;
  puntoControl: number;
  critico: boolean;
}
```

## Servicio

```text
insumos.ts
```

## Endpoints

### Listar todos

```http
GET /v1/insumos
```

### Obtener uno

```http
GET /v1/insumos/{id}
```

### Crear

```http
POST /v1/insumos
```

### Modificar

```http
PUT /v1/insumos/{id}
```

### Eliminar

```http
DELETE /v1/insumos/{id}
```

### Obtener críticos

```http
GET /v1/insumos/criticos
```

### Obtener por categoría

```http
GET /v1/insumos/categoria/{categoriaId}
```

## Body de creación/modificación

```json
{
  "nombre": "Adrenalina 1mg",
  "categoriaId": 1,
  "puntoControl": 20,
  "critico": true
}
```

## Consideraciones

El frontend debe utilizar los nombres del DTO:

```text
puntoControl
esCritico
categoria
```

y no los nombres antiguos provenientes del mock:

```text
punto_control
critico
categoria_id
```

El `puntoControl` representa la cantidad esperada para realizar el control del insumo.

Los insumos críticos necesitan una identificación visual clara.

El oxígeno se modela como un insumo crítico dentro del mismo sistema de control.

---

# 7. Etapa 3: Ambulancias

## Dependencia

Una ambulancia posee un conjunto de insumos.

```text
Insumos
   ↓
Ambulancia
```

Por esa razón se recomienda desarrollar Ambulancias después del catálogo de insumos.

## Página

```text
AdminAmbulancias.tsx
```

## Interface

```text
Ambulancia.ts
```

## Servicio

```text
ambulancias.ts
```

## Endpoints

### Listar

```http
GET /v1/ambulancias
```

### Obtener

```http
GET /v1/ambulancias/{id}
```

### Crear

```http
POST /v1/ambulancias
```

### Modificar

```http
PUT /v1/ambulancias/{id}
```

### Eliminar

```http
DELETE /v1/ambulancias/{id}
```

## Request

```json
{
  "patente": "AB123CD",
  "disponible": true,
  "insumos": [1, 2, 3, 4]
}
```

## Funciones de la pantalla

La administración debería permitir:

- listar ambulancias;
- registrar ambulancia;
- editar patente;
- establecer disponibilidad;
- asignar insumos;
- quitar insumos;
- eliminar una ambulancia;
- visualizar los insumos de cada unidad.

## Consideración importante

Los insumos asociados a la ambulancia son fundamentales para el proceso operativo.

Cuando se asigna una ambulancia a un turno, el backend genera los controles de insumos correspondientes tomando como referencia los insumos configurados para esa ambulancia.

Por lo tanto:

```text
Catálogo de Insumos
        ↓
Ambulancia
        ↓
Insumos asignados
        ↓
Creación del Turno
        ↓
Control de Insumos
```

---

# 8. Etapa 4: Usuarios

## Página

```text
AdminUsuarios.tsx
```

## Interface

```text
Usuario.ts
```

## Servicio

```text
usuarios.ts
```

## Endpoints

### Listar

```http
GET /v1/usuarios
```

### Obtener

```http
GET /v1/usuarios/{id}
```

### Crear

```http
POST /v1/usuarios
```

### Modificar

```http
PUT /v1/usuarios/{id}
```

### Eliminar

```http
DELETE /v1/usuarios/{id}
```

## Request

```json
{
  "nombre": "Nombre Apellido",
  "dni": "12345678",
  "email": "usuario@control107.com",
  "rol": "ENFERMERO",
  "clave": "contraseña",
  "activo": true
}
```

## Roles

```text
ADMINISTRADOR
ENFERMERO
```

## Funciones necesarias

El administrador debe poder:

- crear usuarios;
- editar usuarios;
- consultar usuarios;
- activar/desactivar usuarios;
- eliminar usuarios.

## Recomendación

No utilizar un `input` libre para seleccionar rol.

Utilizar:

```tsx
<select>
  <option value="ADMINISTRADOR">Administrador</option>
  <option value="ENFERMERO">Enfermero</option>
</select>
```

Esto evita enviar valores desconocidos por el enum Java.

---

# 9. Etapa 5: Gestión de Turnos

Este módulo debe desarrollarse una vez que funcionen correctamente:

```text
Usuarios
Ambulancias
Insumos
```

porque un turno relaciona estas entidades.

## Página

```text
AdminTurnos.tsx
```

## Interface

```text
Turno.ts
```

## Servicio

```text
turnos.ts
```

## Endpoints principales

### Listar

```http
GET /v1/turnos
```

### Obtener

```http
GET /v1/turnos/{id}
```

### Crear

```http
POST /v1/turnos
```

### Modificar

```http
PUT /v1/turnos/{id}
```

### Turnos activos

```http
GET /v1/turnos/activos
```

### Turnos por enfermero

```http
GET /v1/turnos/enfermero/{enfermeroId}
```

## Request

```json
{
  "fecha": "2026-10-23",
  "horario": "MANIANA",
  "adminId": 1,
  "enfermeroId": 2,
  "ambulanciaId": 4,
  "nombreChofer": "Nombre Chofer",
  "nombreMedico": "Nombre Médico"
}
```

No es necesario que el frontend establezca:

```text
estado = PROGRAMADO
```

como decisión propia.

El backend construye el nuevo turno en estado `PROGRAMADO`.

---

# 10. Reglas de programación de turnos

El frontend debe conocer estas reglas para mejorar la experiencia de usuario, pero la validación definitiva corresponde al backend.

## Franja horaria

Los valores permitidos son:

```text
MANIANA
TARDE
NOCHE
```

Las franjas definidas en el proyecto son:

```text
MANIANA    06:00 - 14:00
TARDE      14:00 - 22:00
NOCHE      22:00 - 06:00
```

La franja nocturna se considera un único turno operativo.

## Exclusividad del enfermero

Un enfermero no puede participar en dos turnos que tengan simultáneamente:

```text
misma fecha
+
misma franja
```

si el turno existente no está cancelado.

## Exclusividad de ambulancia

Una ambulancia tampoco puede estar asignada a dos turnos con:

```text
misma fecha
+
misma franja
```

si el turno existente no está cancelado.

## Ejemplo

```text
23/10 | MANIANA | Enfermero 2 | Ambulancia 1
```

Impide crear:

```text
23/10 | MANIANA | Enfermero 2 | Ambulancia 2
```

por conflicto de enfermero.

También impide:

```text
23/10 | MANIANA | Enfermero 3 | Ambulancia 1
```

por conflicto de ambulancia.

Pero una combinación en otra franja no presenta ese mismo conflicto:

```text
23/10 | TARDE | Enfermero 2 | Ambulancia 1
```

## Recomendación frontend

Cuando el administrador seleccione:

```text
fecha + horario
```

es conveniente mostrar claramente qué enfermero y ambulancia está seleccionando.

Si posteriormente se implementa disponibilidad preventiva en la UI, debe considerarse una ayuda visual.

La validación definitiva debe seguir quedando en Spring Boot.

---

# 11. Etapa 6: Operativo del Enfermero

Este es el núcleo operativo del MVP.

La documentación establece que debería concentrarse en una pantalla para minimizar la carga de trabajo del enfermero.

## Página

```text
OperativoEnfermero.tsx
```

## Componentes

```text
Operativo/
├── IngresoForm.tsx
├── RestockForm.tsx
├── EgresoForm.tsx
└── ObservacionesForm.tsx
```

## Flujo

```text
PROGRAMADO
     ↓
Control de ingreso
     ↓
EN_CURSO
     ↓
Guardia / reposiciones
     ↓
Control de egreso
     ↓
FINALIZADO
```

Existe además:

```text
PROGRAMADO
     ↓
Cancelación
     ↓
CANCELADO
```

---

# 12. Etapa 6.1: Control de ingreso

## Endpoint

```http
POST /v1/turnos/ingreso
```

## Request

```json
{
  "turnoId": 1,
  "insumos": [
    {
      "id": 1,
      "cantidad": 20,
      "cantidadRestockeo": 0
    }
  ],
  "observaciones": "Sin observaciones"
}
```

## Regla operativa

El turno debe estar:

```text
PROGRAMADO
```

Al registrar correctamente el ingreso pasa a:

```text
EN_CURSO
```

El backend calcula:

```text
faltante = max(0, puntoControl - cantidadIngreso)
```

## Recomendación frontend

No hardcodear:

```ts
{ id: 1, cantidad: ... }
{ id: 3, cantidad: ... }
```

Los insumos deben obtenerse del turno/ambulancia y representarse dinámicamente.

---

# 13. Etapa 6.2: Insumos críticos

Los controles del turno contienen información sobre:

```text
nombre
categoria
esCritico
cantidadIngreso
cantidadEgreso
ingresoFaltante
cantidadUsada
cantidadRestockeo
```

El frontend debería destacar:

```text
esCritico === true
```

especialmente cuando:

```text
ingresoFaltante > 0
```

La documentación del MVP establece que un faltante crítico puede motivar la cancelación del turno.

El oxígeno debe contar con una presentación visual especialmente clara por su importancia operativa.

---

# 14. Etapa 6.3: Reposición

Durante el turno el enfermero puede declarar material recibido adicionalmente.

El modelo utiliza:

```text
cantidadRestockeo
```

El consumo final se calcula conceptualmente mediante:

```text
cantidadIngreso
+
cantidadRestockeo
-
cantidadEgreso
=
cantidadUsada
```

La lógica de cálculo debe permanecer en el backend.

El frontend únicamente recoge y presenta los datos.

---

# 15. Etapa 6.4: Control de egreso

## Endpoint

```http
POST /v1/turnos/egreso
```

El turno debe encontrarse:

```text
EN_CURSO
```

Después del egreso pasa a:

```text
FINALIZADO
```

La UI debería mostrar:

- cantidad de ingreso;
- reposición;
- cantidad de egreso;
- cantidad utilizada;
- observaciones.

---

# 16. Etapa 6.5: Cancelación

## Endpoint

```http
POST /v1/turnos/{id}/cancelar
```

Body:

```json
{
  "observaciones": "Motivo de cancelación"
}
```

Según el backend actual, solamente puede cancelarse un turno que se encuentre en estado:

```text
PROGRAMADO
```

Por tanto, el botón de cancelación no debería presentarse como una operación normal sobre un turno ya finalizado.

---

# 17. Etapa 7: Autenticación y sesión

El módulo de autenticación está definido como parte prioritaria del MVP.

## Página

```text
Login.tsx
```

## Servicio

```text
auth.ts
```

## Interface

```text
Auth.ts
```

## Endpoint

```http
POST /v1/auth/login
```

## Request

```json
{
  "mail": "usuario@email.com",
  "clave": "contraseña"
}
```

## Response

```json
{
  "access_token": "...",
  "expires_in": 3600000,
  "token_type": "Bearer",
  "scope": "..."
}
```

## JWT

El contrato OpenAPI documenta autenticación Bearer:

```http
Authorization: Bearer <token>
```

El JWT generado por el backend incluye información del rol y mail del usuario.

## Roles

La navegación debería diferenciar como mínimo:

```text
ADMINISTRADOR
ENFERMERO
```

Conceptualmente:

```text
Login
  ↓
JWT
  ↓
Rol
 ┌──────────────┴─────────────┐
 ↓                            ↓
ADMINISTRADOR             ENFERMERO
 ↓                            ↓
Administración          Operativo
```

## Advertencia sobre el backend actual

La documentación funcional establece control de acceso según roles.

Sin embargo, antes de considerar terminada esta etapa debe verificarse la configuración de seguridad Spring actualmente desplegada y comprobar mediante pruebas reales que las restricciones de autorización estén efectivamente aplicadas.

El frontend nunca debe considerarse el mecanismo de seguridad.

Ocultar una ruta o un botón según el rol mejora la interfaz, pero la autorización real debe producirse en el backend.

---

# 18. Etapa 8: Historial

## Página

```text
AdminHistorial.tsx
```

El backend proporciona actualmente:

```http
GET /v1/turnos
```

```http
GET /v1/turnos/{id}
```

```http
GET /v1/turnos/enfermero/{enfermeroId}
```

El `TurnoDTO` incluye:

```text
fecha
horario
estado
administrador
enfermero
médico
chofer
ambulancia
observacionesIngreso
observacionesEgreso
controlInsumos
```

Por tanto, una primera versión del historial puede implementarse directamente sobre los turnos existentes.

## Vista recomendada

Listado:

```text
Fecha
Horario
Ambulancia
Enfermero
Estado
```

Detalle:

```text
Datos del turno

Ambulancia
Personal
Observaciones

Control de insumos

Ingreso
Faltante
Reposición
Egreso
Utilizado
```

## Importante

El alcance final del MVP establece que no se comparan automáticamente turnos entre sí.

La trazabilidad se concentra en la información registrada dentro de cada turno.

---

# 19. Etapa 9: Dashboard

## Página

```text
AdminDashboard.tsx
```

Este módulo debe desarrollarse después del flujo operativo porque necesita datos generados por los demás módulos.

## Endpoint disponible

```http
GET /v1/turnos/resumen
```

Devuelve:

```text
ResumenOperativoDTO
```

con:

```text
turnosActivos
ambulanciasDisponibles
ambulanciasTotales
alertas
turnosConInconsistencias
listaAmbulancias
```

## Uso recomendado

La primera versión del dashboard debería utilizar exclusivamente estos datos reales.

Evitar valores hardcodeados como:

```text
4 móviles disponibles
1 móvil requiere revisión
Gasas: 120
```

si no son obtenidos del backend.

---

# 20. Orden final recomendado

## Fase 0 - Base técnica

```text
API_URL
interfaces
manejo común de errores
cliente HTTP
```

## Fase 1 - Catálogo

```text
Categorías
    ↓
Insumos
```

## Fase 2 - Recursos

```text
Ambulancias
Usuarios
```

## Fase 3 - Planificación

```text
Turnos
```

## Fase 4 - Operación

```text
Turno PROGRAMADO
       ↓
Control ingreso
       ↓
EN_CURSO
       ↓
Reposiciones
       ↓
Control egreso
       ↓
FINALIZADO
```

Con camino alternativo:

```text
PROGRAMADO
     ↓
CANCELADO
```

## Fase 5 - Seguridad

```text
Login
JWT
Usuario actual
Roles
Rutas protegidas
```

La estructura básica de autenticación puede prepararse antes, pero se recomienda validar el control de acceso real del backend antes de considerarla finalizada.

## Fase 6 - Consulta

```text
Historial
```

## Fase 7 - Información administrativa

```text
Dashboard
Estadísticas disponibles
Alertas
```

---

# 21. Prioridad práctica de pantallas

Orden sugerido de implementación:

```text
1. Infraestructura API
2. AdminCategorias
3. AdminInsumos
4. AdminAmbulancias
5. AdminUsuarios
6. AdminTurnos
7. OperativoEnfermero
8. Login
9. AdminHistorial
10. AdminDashboard
11. Home / navegación definitiva
```

Este orden prioriza dependencias funcionales.

No representa necesariamente el orden de prioridad de los requerimientos del sistema.

---

# 22. Prioridad según módulos funcionales

El MVP documenta tres grandes módulos:

```text
1. Autenticación
2. Operativo del Enfermero
3. Administrativo
```

El módulo administrativo incluye:

```text
ABM Usuarios
ABM Ambulancias
ABM Insumos
ABM Categorías
Gestión de Turnos
Historial
Dashboard
```

El frontend debe terminar reflejando esa separación independientemente del orden interno utilizado durante el desarrollo.

---

# 23. Recomendaciones generales

## No utilizar `any` permanentemente

Durante la migración del mock puede tolerarse temporalmente:

```ts
useState<any[]>([])
```

pero debe reemplazarse por:

```ts
useState<Usuario[]>([])
useState<Ambulancia[]>([])
useState<Insumo[]>([])
useState<Turno[]>([])
```

---

## Separar DTO de respuesta y request

Por ejemplo:

```text
Ambulancia
AmbulanciaRequest

Insumo
InsumoRequest

Usuario
CrearUsuarioRequest
EditarUsuarioRequest

Turno
TurnoRequest
```

El objeto que devuelve Spring no necesariamente tiene la misma estructura que el objeto enviado.

---

## No hardcodear IDs

Evitar:

```ts
adminId: 1
enfermeroId: 2
ambulanciaId: 4
insumoId: 1
```

Los IDs deben proceder de datos obtenidos de la API o, cuando corresponda, del usuario autenticado.

---

## No hardcodear datos operativos

Evitar en las pantallas definitivas:

```text
Gasas = 120
Ambulancias disponibles = 4
Turno = 1
```

La aplicación debe representar el estado real devuelto por el backend.

---

## Validar `res.ok`

Nunca asumir que:

```ts
await res.json()
```

significa que la operación fue correcta.

Utilizar:

```ts
if (!res.ok) {
  // procesar ErrorDTO
}
```

El backend utiliza una estructura de error con información como estado, error y detalles.

---

## No duplicar reglas de negocio importantes

El frontend puede ayudar a prevenir errores, pero reglas como:

```text
enfermero ocupado
ambulancia ocupada
estado permitido del turno
roles
unicidad
```

deben seguir siendo responsabilidad definitiva del backend.

---

## Formularios dinámicos

El control operativo no debe utilizar insumos fijos escritos en React.

Evitar:

```ts
[
  { id: 1, cantidad: gasas },
  { id: 3, cantidad: oxigeno }
]
```

El formulario debe construirse usando los controles correspondientes al turno.

---

## Mantener el contrato sincronizado

La referencia técnica de integración es:

```text
/api/v3/api-docs
```

Cuando cambie el backend:

```text
Backend cambia
      ↓
Regenerar api-docs.json
      ↓
Revisar interfaces TypeScript
      ↓
Revisar services
      ↓
Revisar páginas afectadas
```

---

# 24. Aspectos del backend a verificar antes de finalizar el frontend

## OpenAPI y DTO de Ambulancias

Se debe mantener sincronizada la especificación OpenAPI con el DTO Java realmente utilizado por el backend.

Antes de cerrar el módulo Ambulancias conviene volver a exportar:

```text
/api/v3/api-docs
```

y verificar que documente todos los campos realmente devueltos.

---

## Seguridad

La documentación requiere:

```text
autenticación
+
autorización por roles
```

Antes de cerrar Login y rutas protegidas debe comprobarse que dichas restricciones se encuentren efectivamente activas en Spring Security.

---

## Usuario autenticado

Mientras no esté completado Login pueden existir IDs administrativos temporales durante desarrollo.

Estos valores deben desaparecer de la versión final.

Por ejemplo:

```ts
adminId: 1
```

deberá sustituirse por el identificador correspondiente al usuario autenticado cuando la integración de seguridad esté terminada.

---

# 25. Criterio para considerar terminado cada módulo

Un módulo no debería considerarse terminado solamente porque renderiza correctamente.

Para cada módulo verificar:

```text
[ ] Interface TypeScript correcta
[ ] Service conectado a Spring
[ ] GET funcionando
[ ] POST funcionando cuando corresponda
[ ] PUT funcionando cuando corresponda
[ ] DELETE funcionando cuando corresponda
[ ] Errores HTTP visibles
[ ] Loading state
[ ] Empty state
[ ] Sin datos mock
[ ] Sin IDs hardcodeados
[ ] Validaciones básicas de formulario
[ ] Validación definitiva realizada por backend
[ ] UI coherente con los estados reales
```

---

# 26. Resultado esperado del MVP frontend

Al completar estas etapas debe ser posible realizar el flujo completo:

```text
Administrador
      ↓
Gestiona categorías
      ↓
Gestiona insumos
      ↓
Configura ambulancias e insumos
      ↓
Gestiona usuarios
      ↓
Programa turno
      ↓
Asigna enfermero + ambulancia
      ↓
Turno PROGRAMADO
      ↓
Enfermero
      ↓
Control de ingreso
      ↓
Turno EN_CURSO
      ↓
Registra reposiciones / operación
      ↓
Control de egreso
      ↓
Turno FINALIZADO
      ↓
Historial
      ↓
Dashboard / resumen operativo
```

El frontend debe facilitar este proceso, mientras que las reglas de negocio, validaciones críticas y persistencia permanecen centralizadas en el backend.