import type { Producto, ProductoNuevo } from "./types/producto";
import type { UnidadMedida } from "./types/unidadMedida";


const API_URL = "http://127.0.0.1:8000/api/v1"

async function obtenerError(response: Response): Promise<string> {
    const data = await response.json()

    return data.detail
}


export async function getProductos(): Promise<Producto[]> {
    const response = await fetch(`${API_URL}/productos/`)

    if (!response.ok) {
        throw new Error(await obtenerError(response))
    }

    return response.json()
}

export async function getUnidades(): Promise<UnidadMedida[]> {
    const response = await fetch(`${API_URL}/unidades-medida`)

    if (!response.ok) {
        throw new Error(await obtenerError(response))
    }

    return response.json()
}

export async function crearProducto(
    producto: ProductoNuevo,
): Promise<Producto> {
    const response = await fetch(`${API_URL}/productos/`, {
        method: "POST",
        headers: {
            "content-Type": "application/json",
        },
        body: JSON.stringify(producto),
    });

    if (!response.ok) {
        throw new Error(await obtenerError(response))
    }

    return response.json();
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
        throw new Error(await obtenerError(response))
    }

    return response.json()
}

export async function anularProducto(id: number): Promise<void> {
    const response = await fetch(`${API_URL}/productos/${id}`, {
        method: "DELETE",
    })

    if (!response.ok) {
        throw new Error(await obtenerError(response))
    }
}
