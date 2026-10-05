import type { Categoria } from "../types/categoria";

interface Props {
    categoria: Categoria;
    onEdit: (categoria: Categoria) => void;
    onDelete: (id: number) => void;
}

export default function CategoriaCard({ categoria, onEdit, onDelete }: Props) {
    return (
        <div className="grid grid-cols-3 items-center border-b border-slate-300 py-3">
            <h2 className="text-slate-800 font-semibold text-lg tracking-wide">{categoria.nombre}</h2>
            <p className="text-slate-600 text-sm mt-1 leading-relaxed">{categoria.descripcion}</p>

            <div className="flex justify-end gap-2 mt-3">
                <button
                    className="bg-gray-600 text-white px-2 py-1 rounded cursor-pointer "
                    onClick={() => onEdit(categoria)}
                >
                    Editar
                </button>

                <button
                    className="bg-red-400 text-white px-2 py-1 rounded cursor-pointer"
                    onClick={() => onDelete(categoria.id)}
                >
                    Eliminar
                </button>
            </div>
        </div>
    );
}
