import type { Producto } from "./types/producto";
import type { UnidadMedida } from "./types/unidadMedida";

const API_URL = "http://127.0.0.1:8000/api/v1"

export async function getProductos(): Promise<Producto[]> {
    const response = await fetch(`${API_URL}/productos/`)

    if (!response.ok) {
        throw new Error("No se pudieron cargar los productos")
    }

    return response.json()
}

export async function getUnidades(): Promise<UnidadMedida[]> {
    const response = await fetch(`${API_URL}/unidades-medida`)

    if (!response.ok) {
        throw new Error("No se pudieron cargar las unidades de medida")
    }

    return response.json()
}

export async function actualizarProducto(
    producto: Producto,
): Promise<Producto> {
    const response = await fetch(`${API_URL}/productos/${producto.id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            nombre: producto.nombre,
            descripcion: producto.descripcion,
            precio_base: producto.precio_base,
            unidad_venta_id: producto.unidad_venta_id,
            stock_cantidad: producto.stock_cantidad,
            disponible: producto.disponible,
        }),
    })

    if (!response.ok) {
        throw new Error("No se pudo actualizar el producto")
    }

    return response.json()
}

export async function anularProducto(id: number): Promise<void>{
    const response = await fetch(`${API_URL}/productos/${id}`,{
    })

    if (!response.ok ){
        throw new Error("No se pudo anular el producto")
}
}