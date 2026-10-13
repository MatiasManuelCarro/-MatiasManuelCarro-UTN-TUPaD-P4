
import { useEffect, useState } from "react";
import type { Categoria, CategoriaData } from "../types/categoria";
import {
    getCategorias,
    createCategoria,
    updateCategoria,
    deleteCategoria,
} from "../services/categorias.service";

export function useCategorias() {
    const [categorias, setCategorias] = useState<Categoria[]>([]);
    const [modalAbierta, setModalAbierta] = useState(false);
    const [categoriaSeleccionada, setCategoriaSeleccionada] =
        useState<Categoria | null>(null);

    useEffect(() => {
        getCategorias().then(setCategorias);
    }, []);

    async function handleCreate(data: CategoriaData) {
        const nueva = await createCategoria(data);
        setCategorias([...categorias, nueva]);
    }

    async function handleUpdate(
        id: number,
        data: CategoriaData
    ) {
        const actualizada = await updateCategoria(id, data);
        setCategorias(categorias.map((c) => (c.id === id ? actualizada : c)));
    }

    async function handleDelete(id: number) {
        await deleteCategoria(id);
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




