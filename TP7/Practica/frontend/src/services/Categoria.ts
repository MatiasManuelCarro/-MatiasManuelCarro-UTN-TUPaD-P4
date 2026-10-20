import type {
    Categoria,
    CategoriaCreate,
    CategoriaPaginatedResponse,
    CategoriaUpdate
} from "../types/Categoria";

const API_URL =
    "http://127.0.0.1:8000/categorias";


export const getCategorias =
    async (): Promise<CategoriaPaginatedResponse> => {
        const response = await fetch(
            `${API_URL}/`
        );

        if (!response.ok) {
            throw new Error(
                "Error al obtener categorías"
            );
        }

        return response.json() as Promise<CategoriaPaginatedResponse>;
    };

export const createCategoria = async (
    categoria: CategoriaCreate,
): Promise<Categoria> => {
    const response = await fetch(
        `${API_URL}/`,
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json",
            },
            body: JSON.stringify(categoria),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Error al crear categoría"
        );
    }

    return response.json() as Promise<Categoria>;
};
export const updateCategoria = async (
    id: number,
    categoria: CategoriaUpdate,
): Promise<Categoria> => {
    const response = await fetch(
        `${API_URL}/${id}`,
        {
            method: "PUT",
            headers: {
                "Content-Type":
                    "application/json",
            },
            body: JSON.stringify(categoria),
        },
    );

    if (!response.ok) {
        throw new Error(
            "Error al actualizar categoría"
        );
    }

    return response.json() as Promise<Categoria>;
};
export const deleteCategoria = async (
    id: number,
): Promise<void> => {
    const response = await fetch(
        `${API_URL}/${id}`,
        {
            method: "DELETE",
        },
    );

    if (!response.ok) {
        throw new Error(
            "Error al eliminar categoría"
        );
    }
};