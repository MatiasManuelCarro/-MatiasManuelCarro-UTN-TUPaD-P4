import { useEffect, useState } from "react";
import type { Categoria } from "../types/categoria";

export function useCategorias() {
    const [categorias, setCategorias] = useState<Categoria[]>([]);
    const [modalAbierta, setModalAbierta] = useState(false);
    const [categoriaSeleccionada, setCategoriaSeleccionada] =
        useState<Categoria | null>(null);

    useEffect(() => {
        fetch("http://localhost:8000/categorias")
            .then((res) => res.json())
            .then((data) => setCategorias(data));
    }, []);

    async function handleCreate(data: { nombre: string; descripcion: string }) {
        const res = await fetch("http://localhost:8000/categorias", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const nueva = await res.json();
        setCategorias([...categorias, nueva]);
    }

    async function handleUpdate(id: number, data: { nombre: string; descripcion: string }) {
        const res = await fetch(`http://localhost:8000/categorias/${id}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        const actualizada = await res.json();
        setCategorias(categorias.map((c) => (c.id === id ? actualizada : c)));
    }

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

    function cerrarModal() {
        setModalAbierta(false);
    }

    return {
        categorias,
        modalAbierta,
        categoriaSeleccionada,
        abrirModalCrear,
        abrirModalEditar,
        cerrarModal,
        handleCreate,
        handleUpdate,
        handleDelete,
    };
}
