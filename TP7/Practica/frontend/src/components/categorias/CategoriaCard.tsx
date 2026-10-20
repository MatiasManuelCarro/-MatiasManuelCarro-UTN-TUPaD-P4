import type { Categoria } from "../../types/Categoria";

type CategoriaCardProps = {
    categoria: Categoria;
    onEdit: (categoria: Categoria) => void;
    onDelete: (id: number) => void;
};

export const CategoriaCard = ({
    categoria,
    onEdit,
    onDelete,
}: CategoriaCardProps) => {
    return (
        <li className="rounded bg-slate-800 p-3 transition-all duration-200 hover:bg-slate-700 hover:shadow-lg hover:-translate-y-0.5">
            <p className="font-semibold">
                {categoria.nombre}
            </p>

            <p className="text-sm text-slate-300">
                {categoria.descripcion || "Sin descripción"}
            </p>

            <div className="mt-3 flex gap-2">
                <button
                    type="button"
                    onClick={() => onEdit(categoria)}
                    className="rounded bg-slate-500 px-3 py-1 text-sm text-white transition-all duration-200 hover:bg-slate-400 cursor-pointer"
                >
                    Editar
                </button>

                <button
                    type="button"
                    onClick={() => onDelete(categoria.id)}
                    className="rounded bg-red-600 px-3 py-1 text-sm text-white transition-all duration-200 hover:bg-red-500 cursor-pointer"
                >
                    Eliminar
                </button>
            </div>
        </li>
    );
};