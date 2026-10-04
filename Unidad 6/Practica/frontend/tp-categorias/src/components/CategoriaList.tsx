import type { Categoria } from "../types/categoria";
import CategoriaCard from "./CategoriaCard";

interface Props {
    categorias: Categoria[];
    onEdit: (categoria: Categoria) => void;
    onDelete: (id: number) => void;
}

export default function CategoriaList({ categorias, onEdit, onDelete }: Props) {
    return (
        <div className="mt-8 flex justify-center">
            <div className="w-full max-w-xl flex flex-col gap-4 
                      bg-neutral-100 border border-neutral-300 
                      rounded-xl p-6 shadow-sm">
                {categorias.map((cat) => (
                    <CategoriaCard
                        key={cat.id}
                        categoria={cat}
                        onEdit={onEdit}
                        onDelete={onDelete}
                    />
                ))}
            </div>
        </div>
    );
}
