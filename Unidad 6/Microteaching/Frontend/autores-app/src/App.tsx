import { useState } from "react";
import type { Autor } from "./types/autor";
import { AutorList } from "./components/AutorList";
import { AutorForm } from "./components/AutorForm";

const iniciales: Autor[] = [
  { id: 1, nombre: "Jorge Luis Borges" },
  { id: 2, nombre: "Julio Cortázar" }
];

export function App() {
  const [autores, setAutores] = useState<Autor[]>(iniciales);

  function agregarAutor(nombre: string){
    setAutores(prev => [...prev, {id: prev.length +1, nombre}])
  }

  return (
    <main>
      <h1>Autores</h1>
      <AutorForm onAgregar={agregarAutor}/>
      <AutorList autores={autores} />
    </main>
  );
}

export default App;
