import type { ProductoPaginatedResponse } from "../types/producto";

export const getProducts = async (): Promise<ProductoPaginatedResponse> => {
    const res = await fetch("http://127.0.0.1:8000/productos?offset=0&limit=10");

    if (!res.ok) {
        throw new Error("Error al cargar productos");
    }

    return res.json(); // ← IMPORTANTE: los paréntesis
};
