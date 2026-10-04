# Mini proyecto Vite + React + TypeScript (hooks) — archivo por archivo

Vamos a ir **archivo por archivo** viendo:
- el **código**
- **cómo funciona**
- y **por qué está hecho así**

---

## 1. `src/main.tsx`

### Código

```Ts
import React from "react"
import ReactDOM from "react-dom/client"
import App from "./App"

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
```

### Cómo funciona

- `ReactDOM.createRoot(...)` crea la **raíz de React** en el elemento con id `"root"` del `index.html`.
- `.render(<React.StrictMode><App /></React.StrictMode>)` le dice a React:
  - renderizá el componente `App`
  - envolvelo en `StrictMode` (modo estricto) para detectar problemas.

### Por qué está hecho así

- `main.tsx` es el **punto de entrada** de la app.
- `App` es el **componente raíz**: desde ahí cuelga todo.
- `StrictMode` ayuda a ver re-render dobles y efectos ejecutados dos veces en desarrollo, lo cual es útil para entender `useEffect`.

---

## 2. `src/App.tsx`

### Código

```Ts
import Counter from "./components/Counter"

function App() {
  return (
    <div>
      <h1>Mini proyecto de hooks</h1>
      <Counter />
    </div>
  )
}

export default App
```

### Cómo funciona

- Importa `Counter`, que es el componente donde vamos a jugar con `useState` y `useEffect`.
- Renderiza un título y el contador.

### Por qué está hecho así

- `App` no tiene lógica complicada: su rol es ser **contenedor**.
- La lógica de hooks vive en `Counter`, así queda más claro qué hace cada cosa.
- Separar responsabilidades: `App` organiza, `Counter` demuestra hooks.

---

## 3. `src/components/Counter.tsx`

### Código

```Ts
import { useState, useEffect } from "react"

function Counter() {
  const [count, setCount] = useState<number>(0)

  // 1) Efecto que se ejecuta solo al montar
  useEffect(() => {
    console.log("Componente Counter montado")
  }, [])

  // 2) Efecto que se ejecuta cuando cambia count
  useEffect(() => {
    console.log("El contador cambió:", count)
  }, [count])

  // 3) Efecto con cleanup
  useEffect(() => {
    console.log("Efecto activo con cleanup, count:", count)

    return () => {
      console.log("Cleanup antes del próximo efecto, count era:", count)
    }
  }, [count])

  return (
    <div>
      <p>Valor actual: {count}</p>
      <button onClick={() => setCount(count + 1)}>
        Incrementar
      </button>
    </div>
  )
}

export default Counter
```

### Cómo funciona

**Estado:**

- `const [count, setCount] = useState<number>(0)`:
  - `count` es el **valor actual** del contador.
  - `setCount` es la **función que actualiza** ese valor.
  - `0` es el **estado inicial**.

Cada vez que llamás `setCount`, React:
- guarda el nuevo valor
- marca el componente para re-render
- vuelve a ejecutar `Counter` y actualiza la UI.

---

**Efecto 1 — solo al montar:**

```Ts
useEffect(() => {
  console.log("Componente Counter montado")
}, [])
```

- El array `[]` indica: **solo una vez**, cuando el componente se monta.
- Sirve para inicializar cosas: logs, fetch inicial, etc.

---

**Efecto 2 — cuando cambia `count`:**

```Ts
useEffect(() => {
  console.log("El contador cambió:", count)
}, [count])
```

- Se ejecuta:
  - al montar
  - cada vez que `count` cambia.
- Muestra cómo `useEffect` **reacciona a cambios de estado**.

---

**Efecto 3 — con cleanup:**

```Ts
useEffect(() => {
  console.log("Efecto activo con cleanup, count:", count)

  return () => {
    console.log("Cleanup antes del próximo efecto, count era:", count)
  }
}, [count])
```

- La función que devolvés (`return () => { ... }`) es el **cleanup**.
- React la ejecuta:
  - antes de volver a correr este efecto
  - cuando el componente se desmonta.
- Esto sirve para:
  - limpiar timers
  - remover event listeners
  - cancelar peticiones, etc.

En este ejemplo, lo usamos para que veas **claramente en consola** el orden:
- efecto activo
- cleanup
- nuevo efecto

---

### Por qué está hecho así

- `Counter` concentra:
  - estado (`useState`)
  - efectos (`useEffect`)
  - cleanup
- Es un ejemplo mínimo pero completo del **ciclo de vida funcional**:
  - montar
  - actualizar
  - desmontar
- Los logs en consola te muestran **qué pasa realmente** cuando:
  - hacés click
  - cambia el estado
  - React re-renderiza
  - se ejecutan efectos y cleanups.

---

Si querés, el próximo paso puede ser:
- agregar un **`useEffect` que haga un `setInterval`** y lo limpie con cleanup
- o un **fetch simulado** para ver efectos asíncronos.

---
# Archivo: index.html (Vite + React + TypeScript)

Este archivo es la **base del proyecto**.  
React NO renderiza directamente en el body: necesita un “punto de montaje”.  
Ese punto es el `<div id="root"></div>`.

Sin este archivo, React no tendría dónde dibujar la aplicación.

---

## Código completo de index.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Mini Hooks</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

---

## ¿Cómo funciona?

### 1. `<div id="root"></div>`
Este es el **contenedor donde React va a renderizar tu aplicación**.

En `main.tsx` tenés:

```ts
ReactDOM.createRoot(document.getElementById("root") as HTMLElement)
  .render(<App />)
```

Eso significa:

- Buscá el elemento con id `"root"`
- Montá ahí toda la aplicación React

Sin este div, React no puede renderizar nada.

---

### 2. `<script type="module" src="/src/main.tsx"></script>`
Vite permite importar módulos ES directamente desde HTML.

Este script:

- carga tu archivo `main.tsx`
- inicializa React
- monta la app en el DOM

Es la **puerta de entrada** al proyecto.

---

### 3. `<link rel="icon" href="/vite.svg" />`
El favicon del proyecto.  
No afecta la lógica, pero Vite lo incluye por defecto.

---

### 4. `<meta name="viewport">`
Hace que la app sea responsive en móviles.

---

## ¿Por qué está hecho así?

- Vite usa **ES Modules nativos**, por eso el script apunta directo a `main.tsx`.
- React necesita un **root** para renderizar.
- El HTML es mínimo porque **todo lo demás lo maneja React**.
- A diferencia de CRA, Vite no oculta nada: vos ves el HTML real.

---

## Resumen

- `index.html` es el archivo base del proyecto.
- Define el contenedor donde React va a renderizar (`#root`).
- Carga el archivo `main.tsx`, que inicia la app.
- Es simple, directo y transparente (a diferencia de CRA).

