import type { Producto } from "./types/producto";
import type { UnidadMedida } from "./types/unidadMedida";

const API_URL = "http://127.0.0.1:8000/api/v1"

export async function getProductos(): Promise<Producto[]>{
    const response = await fetch(`${API_URL}/productos/`)

    if (!response.ok){
        throw new Error("No se pudieron cargar los productos")
    }

    return response.json()
}

export async function getUnidades(): Promise<UnidadMedida[]>{
    const response = await fetch(`${API_URL}/unidades-medida`)

    if (!response.ok){
        throw new Error("No se pudieron cargar las unidades de medida")
    }

    return response.json()
}