import type { Categoria } from "../types/categoria";
import CategoriaCard from "./CategoriaCard";

interface Props {
    categorias: Categoria[];
    onEdit: (categoria: Categoria) => void;
    onDelete: (id: number) => void;
}

export default function CategoriaList({ categorias, onEdit, onDelete }: Props) {
    return (
        <div className="w-full flex flex-col">

            {/* Encabezado de tabla */}
            <div className="grid grid-cols-3 border-b border-slate-300 py-2 px-1 bg-slate-100 rounded-t-xl">
                <div className="text-slate-700 font-semibold">Nombre</div>
                <div className="text-slate-700 font-semibold">Descripción</div>
                <div className="text-slate-700 font-semibold text-right">Acciones</div>
            </div>

            {/* Filas */}
            {categorias.map((cat) => (
                <CategoriaCard
                    key={cat.id}
                    categoria={cat}
                    onEdit={onEdit}
                    onDelete={onDelete}
                />
            ))}
        </div>
    );
}
