import type { CategoriaData } from "../types/categoria";


export async function getCategorias() {
    const res = await fetch("http://localhost:8000/categorias");
    return res.json();
}

export async function createCategoria(data: CategoriaData) {
    const res = await fetch("http://localhost:8000/categorias", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    return res.json();
}

export async function updateCategoria(id: number, data: CategoriaData) {
    const res = await fetch(`http://localhost:8000/categorias/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
    });
    return res.json();
}

export async function deleteCategoria(id: number) {
    return fetch(`http://localhost:8000/categorias/${id}`, {
        method: "DELETE",
    });
}
