# 📘 API 107 — Endpoints en formato JSON
Documentación generada a partir del OpenAPI que me pasaste.

Cada endpoint está expresado como un objeto JSON usando ````` para que puedas reemplazarlo fácilmente.

---

# 🟥 USUARIOS

## ✔ GET — Listar usuarios
```json
{
  "method": "GET",
  "url": "/v1/usuarios",
  "response": [
    {
      "id": 1,
      "nombre": "Juan Gómez",
      "dni": "12345678",
      "email": "juan@107.com",
      "rol": "ENFERMERO",
      "activo": true
    }
  ]
}
```

---

## ✔ POST — Crear usuario
```json
{
  "method": "POST",
  "url": "/v1/usuarios",
  "body": {
    "nombre": "Juan Gómez",
    "dni": "12345678",
    "email": "juan@107.com",
    "rol": "ENFERMERO",
    "clave": "123456",
    "activo": true
  },
  "response": {
    "id": 1,
    "nombre": "Juan Gómez",
    "dni": "12345678",
    "email": "juan@107.com",
    "rol": "ENFERMERO",
    "activo": true
  }
}
```

---

## ✔ GET — Obtener usuario por ID
```json
{
  "method": "GET",
  "url": "/v1/usuarios/1",
  "response": {
    "id": 1,
    "nombre": "Juan Gómez",
    "dni": "12345678",
    "email": "juan@107.com",
    "rol": "ENFERMERO",
    "activo": true
  }
}
```

---

## ✔ PUT — Actualizar usuario
```json
{
  "method": "PUT",
  "url": "/v1/usuarios/1",
  "body": {
    "nombre": "Juan Gómez",
    "dni": "12345678",
    "email": "juan@107.com",
    "rol": "ADMINISTRADOR",
    "clave": "nuevaClave",
    "activo": true
  },
  "response": {
    "id": 1,
    "nombre": "Juan Gómez",
    "dni": "12345678",
    "email": "juan@107.com",
    "rol": "ADMINISTRADOR",
    "activo": true
  }
}
```

---

## ✔ DELETE — Eliminar usuario
```json
{
  "method": "DELETE",
  "url": "/v1/usuarios/1",
  "response": {
    "status": "OK"
  }
}
```

---

# 🟦 AMBULANCIAS

## ✔ GET — Listar ambulancias
```json
{
  "method": "GET",
  "url": "/v1/ambulancias",
  "response": [
    {
      "id": 1,
      "patente": "AA123BB"
    }
  ]
}
```

---

## ✔ POST — Crear ambulancia
```json
{
  "method": "POST",
  "url": "/v1/ambulancias",
  "body": {
    "patente": "AA123BB",
    "disponible": true,
    "insumos": [1, 2, 3]
  },
  "response": {
    "id": 1,
    "patente": "AA123BB"
  }
}
```

---

## ✔ GET — Obtener ambulancia por ID
```json
{
  "method": "GET",
  "url": "/v1/ambulancias/1",
  "response": {
    "id": 1,
    "patente": "AA123BB"
  }
}
```

---

## ✔ PUT — Actualizar ambulancia
```json
{
  "method": "PUT",
  "url": "/v1/ambulancias/1",
  "body": {
    "patente": "AA123BB",
    "disponible": false,
    "insumos": [1, 2]
  },
  "response": {
    "id": 1,
    "patente": "AA123BB"
  }
}
```

---

## ✔ DELETE — Eliminar ambulancia
```json
{
  "method": "DELETE",
  "url": "/v1/ambulancias/1",
  "response": {
    "status": "OK"
  }
}
```

---

# 🟩 INSUMOS

## ✔ GET — Listar insumos
```json
{
  "method": "GET",
  "url": "/v1/insumos",
  "response": [
    {
      "id": 1,
      "nombre": "Gasas",
      "categoria": "Descartables",
      "puntoControl": 10,
      "esCritico": false
    }
  ]
}
```

---

## ✔ POST — Crear insumo
```json
{
  "method": "POST",
  "url": "/v1/insumos",
  "body": {
    "nombre": "Gasas",
    "categoriaId": 3,
    "puntoControl": 10,
    "critico": false
  },
  "response": {
    "id": 1,
    "nombre": "Gasas",
    "categoria": "Descartables",
    "puntoControl": 10,
    "esCritico": false
  }
}
```

---

## ✔ GET — Obtener insumo por ID
```json
{
  "method": "GET",
  "url": "/v1/insumos/1",
  "response": {
    "id": 1,
    "nombre": "Gasas",
    "categoria": "Descartables",
    "puntoControl": 10,
    "esCritico": false
  }
}
```

---

## ✔ PUT — Actualizar insumo
```json
{
  "method": "PUT",
  "url": "/v1/insumos/1",
  "body": {
    "nombre": "Gasas estériles",
    "categoriaId": 3,
    "puntoControl": 15,
    "critico": true
  },
  "response": {
    "id": 1,
    "nombre": "Gasas estériles",
    "categoria": "Descartables",
    "puntoControl": 15,
    "esCritico": true
  }
}
```

---

## ✔ DELETE — Eliminar insumo
```json
{
  "method": "DELETE",
  "url": "/v1/insumos/1",
  "response": {
    "status": "OK"
  }
}
```

---

# 🟧 CATEGORÍAS DE INSUMOS

## ✔ GET — Listar categorías
```json
{
  "method": "GET",
  "url": "/v1/categorias",
  "response": [
    {
      "id": 1,
      "nombre": "Medicamentos",
      "color": "#FF5555"
    }
  ]
}
```

---

## ✔ POST — Crear categoría
```json
{
  "method": "POST",
  "url": "/v1/categorias",
  "body": {
    "nombre": "Oxígeno",
    "color": "#00AACC"
  },
  "response": {
    "id": 2,
    "nombre": "Oxígeno",
    "color": "#00AACC"
  }
}
```

---

## ✔ GET — Obtener categoría por ID
```json
{
  "method": "GET",
  "url": "/v1/categorias/1",
  "response": {
    "id": 1,
    "nombre": "Medicamentos",
    "color": "#FF5555"
  }
}
```

---

## ✔ PUT — Actualizar categoría
```json
{
  "method": "PUT",
  "url": "/v1/categorias/1",
  "body": {
    "nombre": "Medicamentos críticos",
    "color": "#FF0000"
  },
  "response": {
    "id": 1,
    "nombre": "Medicamentos críticos",
    "color": "#FF0000"
  }
}
```

---

## ✔ DELETE — Eliminar categoría
```json
{
  "method": "DELETE",
  "url": "/v1/categorias/1",
  "response": {
    "status": "OK"
  }
}
```

---

# 🟦 TURNOS

## ✔ GET — Listar turnos
```json
{
  "method": "GET",
  "url": "/v1/turnos",
  "response": [
    {
      "id": 1,
      "fecha": "2026-10-12",
      "horario": "MANIANA",
      "estado": "PROGRAMADO"
    }
  ]
}
```

---

## ✔ POST — Crear turno
```json
{
  "method": "POST",
  "url": "/v1/turnos",
  "body": {
    "fecha": "2026-10-12",
    "horario": "MANIANA",
    "adminId": 1,
    "enfermeroId": 2,
    "ambulanciaId": 3,
    "nombreChofer": "Carlos",
    "nombreMedico": "Dr. Pérez"
  },
  "response": {
    "id": 1,
    "fecha": "2026-10-12",
    "horario": "MANIANA",
    "estado": "PROGRAMADO"
  }
}
```

---

## ✔ GET — Obtener turno por ID
```json
{
  "method": "GET",
  "url": "/v1/turnos/1",
  "response": {
    "id": 1,
    "fecha": "2026-10-12",
    "horario": "MANIANA",
    "estado": "PROGRAMADO"
  }
}
```

---

## ✔ PUT — Actualizar turno
```json
{
  "method": "PUT",
  "url": "/v1/turnos/1",
  "body": {
    "fecha": "2026-10-12",
    "horario": "TARDE",
    "adminId": 1,
    "enfermeroId": 2,
    "ambulanciaId": 3,
    "nombreChofer": "Carlos",
    "nombreMedico": "Dr. Pérez"
  },
  "response": {
    "id": 1,
    "fecha": "2026-10-12",
    "horario": "TARDE",
    "estado": "PROGRAMADO"
  }
}
```

---

# 🟩 ¿Querés que te arme ahora un README separado por carpetas?  
- `/usuarios`  
- `/ambulancias`  
- `/insumos`  
- `/categorias`  
- `/turnos`  

O querés que te arme **los servicios en TypeScript** (`apiUsuarios.ts`, `apiInsumos.ts`, etc.)?

Decime y lo dejo perfecto.