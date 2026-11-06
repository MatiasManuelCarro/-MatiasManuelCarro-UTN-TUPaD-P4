# Food Store - Frontend

Frontend desarrollado por Matias Manuel Carro para el Segundo Parcial de Programación IV.

La aplicación permite administrar el catálogo de productos de Food Store mediante una interfaz web desarrollada con React, TypeScript y Tailwind CSS.

El frontend consume la API REST desarrollada en FastAPI utilizando `fetch` nativo.

## Tecnologías

- React
- TypeScript
- Vite
- Tailwind CSS 4
- Fetch API

## Requisitos previos

Antes de ejecutar el proyecto es necesario tener instalado:

- Node.js
- npm o pnpm

También debe estar en ejecución el backend de Food Store.

Por defecto, el frontend consume la API desde:

```text
http://127.0.0.1:8000/api/v1
```

Esta configuración se encuentra en:

```text
src/api.ts
```

## Instalación

Desde la carpeta:

```text
foodstore-frontend
```

instalar las dependencias utilizando **npm**:

```powershell
npm install
```

O, si se utiliza **pnpm**:

```powershell
pnpm install
```

## Ejecución

Antes de iniciar el frontend, el backend de Food Store debe encontrarse en ejecución.

Con **npm**:

```powershell
npm run dev
```

O con **pnpm**:

```powershell
pnpm dev
```

Vite mostrará en la terminal la dirección local donde se encuentra disponible la aplicación.

## Compilación

Para comprobar que el proyecto compila correctamente, ejecutar:

Con **npm**:

```powershell
npm run build
```

O con **pnpm**:

```powershell
pnpm build
```

La compilación realiza la comprobación de TypeScript y genera la versión de producción mediante Vite.

## Funcionalidades

La interfaz permite administrar los productos del catálogo.

### Listado de productos

Al iniciar la aplicación se cargan los productos desde:

```text
GET /api/v1/productos
```

Cada producto se representa mediante una tarjeta que muestra:

- Nombre.
- Descripción.
- Precio y símbolo de la unidad de venta.
- Stock y símbolo de la unidad de venta.
- Estado de disponibilidad.
- Indicador de existencia de stock.

Cada tarjeta incluye las siguientes acciones:

- Editar.
- Cambiar disponibilidad.
- Anular.

## Alta de productos

El botón `Nuevo Producto` abre el modal con el formulario vacío.

El formulario permite ingresar:

- Nombre.
- Descripción.
- Precio base.
- Stock.
- Unidad de venta.

El selector de unidad de venta utiliza el catálogo obtenido desde:

```text
GET /api/v1/unidades-medida
```

Al crear un producto se realiza:

```text
POST /api/v1/productos
```

Si la operación finaliza correctamente, el nuevo producto se incorpora al listado sin necesidad de recargar la página.

## Edición de productos

El botón `Editar` abre el mismo modal utilizado para el alta, cargando los datos del producto seleccionado.

Al guardar los cambios se realiza:

```text
PUT /api/v1/productos/{id}
```

El producto actualizado reemplaza al anterior en el estado local y la tarjeta refleja los cambios sin recargar la página.

## Disponibilidad

El botón `Disponibilidad` permite pausar o volver a habilitar la venta del producto.

La aplicación invierte el valor actual de:

```text
disponible
```

y actualiza el producto mediante:

```text
PUT /api/v1/productos/{id}
```

Este estado es independiente del stock y de la baja lógica del producto.

## Anulación de productos

El botón `Anular` realiza:

```text
DELETE /api/v1/productos/{id}
```

La eliminación es lógica y es gestionada por el backend.

Cuando la operación finaliza correctamente, el producto se elimina del listado mostrado por el frontend.

## Manejo de errores

Los errores enviados por la API se reciben utilizando el campo:

```json
{
    "detail": "Mensaje de error"
}
```

Los errores producidos durante el alta o la edición se muestran dentro del modal.

Por ejemplo, si se intenta utilizar el nombre de otro producto activo, el backend responde con un conflicto y el modal permanece abierto mostrando el mensaje correspondiente.

## Estados de la interfaz

La aplicación contempla diferentes estados durante el consumo de la API:

- Carga inicial.
- Error al cargar los datos.
- Catálogo sin productos.
- Catálogo con productos.

Cuando no existen productos, la aplicación mantiene disponible el botón `Nuevo Producto` para permitir crear el primero.

## Estado y comunicación entre componentes

El estado principal del catálogo se encuentra en:

```text
src/App.tsx
```

`App` mantiene:

- Lista de productos.
- Lista de unidades de medida.
- Producto seleccionado.
- Estado de apertura del modal.
- Estado de carga.
- Estado de error.

Los componentes hijos reciben los datos mediante props tipadas y comunican las acciones al componente padre mediante funciones recibidas por props.

Los componentes de presentación no realizan consultas directas a la API.

## Estructura principal

```text
src/
├── components/
│   ├── Footer.tsx
│   ├── Navbar.tsx
│   ├── ProductoCard.tsx
│   ├── ProductoList.tsx
│   └── ProductoModal.tsx
├── types/
│   ├── categoria.ts
│   ├── producto.ts
│   └── unidadMedida.ts
├── api.ts
├── App.tsx
├── index.css
└── main.tsx
```

## Componentes

### Navbar

Muestra la identificación de Food Store y el título de administración de productos.

### ProductoList

Recibe la lista de productos mediante props y utiliza `.map()` para renderizar las tarjetas.

### ProductoCard

Representa individualmente cada producto.

Muestra sus datos e indicadores y expone las acciones de edición, disponibilidad y anulación.

### ProductoModal

Modal reutilizado para alta y edición.

Cuando no existe un producto seleccionado, el formulario se inicializa vacío.

Cuando existe un producto seleccionado, el formulario se inicializa con los datos actuales del producto.

### Footer

Muestra información del proyecto 

## Tipos TypeScript

Las interfaces utilizadas por la aplicación se encuentran en:

```text
src/types/
```

Se definen tipos para:

- `Producto`
- `ProductoNuevo`
- `UnidadMedida`
- `Categoria`

Estos tipos representan los datos intercambiados con la API y permiten mantener el proyecto tipado sin utilizar `any`.

## API

Las funciones de acceso al backend están centralizadas en:

```text
src/api.ts
```

Se utiliza `fetch` nativo para las operaciones:

```text
GET     /api/v1/productos
GET     /api/v1/unidades-medida
POST    /api/v1/productos
PUT     /api/v1/productos/{id}
DELETE  /api/v1/productos/{id}
```

El frontend solicita hasta 50 productos utilizando el parámetro `limit` soportado por la API.

## Estilos

La interfaz utiliza Tailwind CSS 4 con un enfoque utility-first.

Los estilos se aplican directamente mediante clases para:

- Contenedores.
- Tarjetas.
- Tipografía.
- Inputs.
- Selectores.
- Botones.
- Indicadores de estado.
- Estados `hover`.
- Estados `disabled`.
- Mensajes de éxito y error.

## Ejecución completa del proyecto

Primero iniciar el backend desde:

```text
foodstore-backend
```

con:

```powershell
fastapi dev app/main.py
```

Luego, desde:

```text
foodstore-frontend
```

instalar las dependencias:

```powershell
npm install
```

e iniciar el frontend:

```powershell
npm run dev
```

Con ambos proyectos ejecutándose, la aplicación web podrá consumir la API y administrar el catálogo de productos.


### Desarrollado por Matias Manuel Carro