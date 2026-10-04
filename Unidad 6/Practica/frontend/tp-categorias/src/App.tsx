import { useEffect, useState } from "react";
import Navbar from "./components/Navbar";
import CategoriaList from "./components/CategoriaList";
import CategoriaModal from "./components/CategoriaModal";
import type { Categoria } from "./types/categoria";

export default function App() {
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [modalAbierta, setModalAbierta] = useState(false);
  const [categoriaSeleccionada, setCategoriaSeleccionada] = useState<Categoria | null>(null);

  // GET inicial
  useEffect(() => {
    fetch("http://localhost:8000/categorias")
      .then((res) => res.json())
      .then((data) => setCategorias(data));
  }, []);

  // Crear
  async function handleCreate(data: { nombre: string; descripcion: string }) {
    const res = await fetch("http://localhost:8000/categorias", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const nueva = await res.json();
    setCategorias([...categorias, nueva]);
  }

  // Editar
  async function handleUpdate(id: number, data: { nombre: string; descripcion: string }) {
    const res = await fetch(`http://localhost:8000/categorias/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    const actualizada = await res.json();
    setCategorias(categorias.map((c) => (c.id === id ? actualizada : c)));
  }

  // Eliminar
  async function handleDelete(id: number) {
    await fetch(`http://localhost:8000/categorias/${id}`, { method: "DELETE" });
    setCategorias(categorias.filter((c) => c.id !== id));
  }

  function abrirModalCrear() {
    setCategoriaSeleccionada(null);
    setModalAbierta(true);
  }

  function abrirModalEditar(cat: Categoria) {
    setCategoriaSeleccionada(cat);
    setModalAbierta(true);
  }

  return (
    <>
      <Navbar />

      <div className="p-4">
        <button
          className="bg-gray-500 text-white px-4 py-2 rounded"
          onClick={abrirModalCrear}
        >
          + Añadir Categoría
        </button>

        <CategoriaList
          categorias={categorias}
          onEdit={abrirModalEditar}
          onDelete={handleDelete}
        />
      </div>

      <CategoriaModal
        abierta={modalAbierta}
        categoria={categoriaSeleccionada}
        onClose={() => setModalAbierta(false)}
        onSubmit={(data) =>
          categoriaSeleccionada
            ? handleUpdate(categoriaSeleccionada.id, data)
            : handleCreate(data)
        }
      />
    </>
  );
}
