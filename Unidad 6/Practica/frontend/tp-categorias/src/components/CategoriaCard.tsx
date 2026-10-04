import type { Categoria } from "../types/categoria";

interface Props {
    categoria: Categoria;
    onEdit: (categoria: Categoria) => void;
    onDelete: (id: number) => void;
}

export default function CategoriaCard({ categoria, onEdit, onDelete }: Props) {
    return (
        <div className="border p-4 rounded shadow">
            <h2 className="font-bold">{categoria.nombre}</h2>
            <p>{categoria.descripcion}</p>

            <div className="flex gap-2 mt-2">
                <button
                    className="bg-gray-600 text-white px-2 py-1 rounded"
                    onClick={() => onEdit(categoria)}
                >
                    Editar
                </button>

                <button
                    className="bg-red-400 text-white px-2 py-1 rounded"
                    onClick={() => onDelete(categoria.id)}
                >
                    Eliminar
                </button>
            </div>
        </div>
    );
}
