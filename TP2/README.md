# README – API REST Spring Boot - TP2 - Programación 4)¿

**Alumno:**
Matias Carro - matiasmanuelcarro@gmail.com 

## 1. Descripción general del proyecto

### Trabajo Práctico - Api Rest

**OBJETIVO GENERAL**

- Desarrollar una API REST completa y profesional para la gestión de productos

- Aplicar arquitectura en capas

- Implementar validaciones

- Implementar manejo de errores

- Implementar persistencia con Spring Data JPA

- Implementar documentación con Swagger
---

# 2. Dependencias principales

## Spring Boot
- Spring Web  
- Spring Data JPA  
- Lombok  
- H2 Database  
- Spring Boot DevTools  

## Swagger (OpenAPI)


implementation 'org.springdoc:springdoc-openapi-starter-webmvc-ui:2.8.8'

Swagger UI esta  disponible en:

http://localhost:8080/swagger-ui.html

---

# 3. Arquitectura del proyecto

El proyecto sigue una arquitectura en capas:

```
 |-- controller/
 |     |-- CategoriaController.java
 |     |-- UsuarioController.java
 |     |-- ProductoController.java
 |     |-- PedidoController.java
 |
 |-- service/
 |     |-- UsuarioService.java
 |     |-- ProductoService.java
 |     |-- CategoriaService.java
 |     |-- PedidoService.java
 |
 |-- repository/
 |     |-- UsuarioRepository.java
 |     |-- ProductoRepository.java
 |     |-- CategoriaRepository.java
 |     |-- PedidoRepository.java
 |
 |-- entities/
 |     |-- Usuario.java
 |     |-- Producto.java
 |     |-- Categoria.java
 |     |-- Pedido.java
 |     |-- DetallePedido.java
 |
 |-- dtos/
       |
       |-- usuario/
       |     |-- UsuarioDto.java
       |     |-- UsuarioCreate.java
       |     |-- UsuarioEdit.java
       |
       |-- producto/
       |     |-- ProductoDto.java
       |     |-- ProductoCreate.java
       |     |-- ProductoEdit.java
       |
       |-- categoria/
       |     |-- CategoriaDto.java
       |     |-- CategoriaCreate.java
       |     |-- CategoriaEdit.java
       |
       |-- pedido/
             |-- PedidoDto.java
             |-- PedidoCreate.java
             |-- PedidoEdit.java
             |-- PedidoCreateConUsuario.java

```

Cada capa tiene una responsabilidad clara.

---

### Entities

Representan las tablas de la base de datos.  

- Usuario
- Producto
- Categoria
- Pedido
- DetallePedido

---

### DTOs (Data Transfer Objects)

Los DTOs permiten:

- Controlar qué datos se exponen  
- Validar entradas  
- Evitar exponer entidades directamente  

**DTOS del proyecto:**

- **usuario/**
  - UsuarioDto.java
  - UsuarioCreate.java
  - UsuarioEdit.java

- **producto/**
  - ProductoDto.java
  - ProductoCreate.java
  - ProductoEdit.java

- **categoria/**
  - CategoriaDto.java
  - CategoriaCreate.java
  - CategoriaEdit.java

- **pedido/**
  - PedidoDto.java
  - PedidoCreate.java
  - PedidoEdit.java
  - PedidoCreateConUsuario.java


---

### Repository

Cada entidad tiene su repositorio:

```java
public interface UsuarioRepository extends JpaRepository<Usuario, Long> {}
```
```java
public interface ProductoRepository extends JpaRepository<Producto, Long> {}
```

```java
public interface CategoriaRepository extends JpaRepository<Categoria, Long> {}
```

```java
public interface PedidoRepository extends JpaRepository<Pedido, Long> {}
```

```java
public interface DetallePedidoRepository extends JpaRepository<DetallePedido, Long> {}
```


Los repositorios permiten:

- Guardar entidades  
- Buscar por ID  
- Buscar por atributos  
- Listar todos  
- Eliminar  

---

### Service

La capa Service implementa la lógica de negocio.

- Validaciones  
- Conversión entre DTO y entidad  
- Manejo de excepciones  
- Reglas de negocio (soft delete, asignación de pedidos, etc.)

Los servicios del documento:

- UsuarioService  
- ProductoService  
- CategoriaService  
- PedidoService  

Cada servicio usa su repositorio y devuelve DTOs.

---

### Controller

Los controladores exponen la API REST.

Ejemplos del documento:

- UsuarioController  
- ProductoController  
- PedidoController  
- CategoriaController  

Cada controlador implementa:

- GET (listar, buscar por ID, buscar por mail)  
- POST (crear)  
- PUT (editar)  
- DELETE (eliminar o soft delete)  

---

### AdviceController (Manejo de errores)

Se implementa un @RestControllerAdvice para capturar excepciones:

- EntityNotFound  
- Validaciones  
- Datos inválidos  
- Errores de negocio  

Ejemplo:

```java
@ExceptionHandler(EntityNotFoundException.class)  
public ResponseEntity<?> handleNotFound(EntityNotFoundException ex)
```
---

# 4. Carga inicial de datos (CommandLineRunner)

El documento incluye un CommandLineRunner que crea datos para pruebas:

- 5 usuarios  
- 5 categorías  
- 10 productos  
- 10 pedidos con detalles  
- Asignación de pedidos a usuarios  


---

# 5. Pruebas con Postman

**Las pruebas con imagenes pueden verse en el PDF que se encuentra en la raiz del proyecto**

### Crear datos (POST)

### Crear usuarios

**Usuario 1**
POST /usuarios
```json
{
  "nombre": "Carolina",
  "apellido": "Gutierrez",
  "mail": "carolina.g@mail.com",
  "celular": "1167894321",
"password": "caro123",
  "rol": "USUARIO"
}
```

**Usuario 2**
POST /usuarios
```json
{
  "nombre": "Roberto",
  "apellido": "Sanchez",
  "mail": "roberto.s@mail.com",
  "celular": "1176543210",
  "password": "rober123",
  "rol": "ADMIN"
}
```

### Crear categorías

**Categoría 1**
POST /categorias
```json
{
  "nombre": "Redes",
  "descripcion": "Routers, switches, placas de red"
}
```
**Categoría 2**
POST /categorias
```json
{
  "nombre": "Impresion",
  "descripcion": "Impresoras, tintas, repuestos"
}
```

**Categoría 3**
POST /categorias
```json
{
  "nombre": "Sillas Gamer",
  "descripcion": "Sillas ergonómicas y gamer"
}
```

***Productos de redes***

POST /productos

```json
{
  "nombre": "Router TP-Link AX1800",
  "precio": 52000,
  "descripcion": "WiFi 6",
  "stock": 25,
  "imagen": "router.jpg",
  "activo": true,
  "idCategoria": 1
}
```
```json
{
  "nombre": "Switch Gigabit 8 Puertos",
  "precio": 35000,
  "descripcion": "1000 Mbps",
  "stock": 40,
  "imagen": "switch.jpg",
  "activo": true,
  "idCategoria": 1
}
```

```json
{
  "nombre": "Placa de Red PCIe",
  "precio": 15000,
  "descripcion": "Gigabit Ethernet",
  "stock": 60,
  "imagen": "nic.jpg",
  "activo": true,
  "idCategoria": 1
}
```

***Productos de Impresión***

```json
{
  "nombre": "Impresora HP DeskJet 2776",
  "precio": 68000,
  "descripcion": "Multifunción WiFi",
  "stock": 15,
  "imagen": "hp.jpg",
  "activo": true,
  "idCategoria": 2
}
```

```json
{
  "nombre": "Cartucho Negro HP 428",
  "precio": 12000,
  "descripcion": "Original",
  "stock": 80,
  "imagen": "cartucho.jpg",
  "activo": true,
  "idCategoria": 2
}
```

```json
{
  "nombre": "Resma A4 80g",
  "precio": 6000,
  "descripcion": "500 hojas",
  "stock": 100,
  "imagen": "resma.jpg",
  "activo": true,
  "idCategoria": 2
}
```

***Productos de Sillas Gamer***
```json
{
  "nombre": "Silla Gamer Razer",
  "precio": 150000,
  "descripcion": "Ergonómica premium",
  "stock": 10,
  "imagen": "razer.jpg",
  "activo": true,
  "idCategoria": 3
}
```
```json
{
  "nombre": "Silla Gamer Redragon",
  "precio": 110000,
  "descripcion": "Cuero sintético",
  "stock": 20,
  "imagen": "redragon.jpg",
  "activo": true,
  "idCategoria": 3
}
```
```json
{
  "nombre": "Silla Gamer Corsair",
  "precio": 130000,
  "descripcion": "Soporte lumbar",
  "stock": 12,
  "imagen": "corsair.jpg",
  "activo": true,
  "idCategoria": 3
}
```
```json
{
  "nombre": "Almohadilla Lumbar",
  "precio": 9000,
  "descripcion": "Memory foam",
  "stock": 50,
  "imagen": "almohadilla.jpg",
  "activo": true,
  "idCategoria": 3
}
```


### Crear pedidos con detalles
POST /pedidos

***Pedido 1 (Usuario 1)***

```json
{
  "fecha": "2026-08-29",
  "estado": "PENDIENTE",
  "formaPago": "EFECTIVO",
  "usuarioId": 1,
  "detalles": [
    { "cantidad": 1, "productoId": 1 },
    { "cantidad": 2, "productoId": 4 }
  ]
}
```

***Pedido 2 (Usuario 2)***
```json
{
  "fecha": "2026-08-29",
  "estado": "CONFIRMADO",
  "formaPago": "TARJETA",
  "usuarioId": 2,
  "detalles": [
    { "cantidad": 3, "productoId": 7 },
    { "cantidad": 1, "productoId": 10 }
  ]
}
```

***Pedido 3 (Usuario 1)***
```json
{
  "fecha": "2026-08-29",
  "estado": "TERMINADO",
  "formaPago": "TRANSFERENCIA",
  "usuarioId": 1,
  "detalles": [
    { "cantidad": 2, "productoId": 3 },
    { "cantidad": 1, "productoId": 9 }
  ]
}
```

---

### Actualizar categoría

PUT /categorias/{id}

Body:

{
  "nombre": "Periféricos Gamer",
  "descripcion": "Teclados y mouse de alta gama"
}

---

### Buscar por ID
GET /usuarios/{id}

### Buscar por mail
GET /usuarios/mail/{mail}

---

# 6. Swagger funcionando

Acceder a:

http://localhost:8080/swagger-ui.html

Swagger muestra:

- Todos los endpoints  
- DTOs  
- Métodos HTTP  
- Ejemplos de request y response  

---

