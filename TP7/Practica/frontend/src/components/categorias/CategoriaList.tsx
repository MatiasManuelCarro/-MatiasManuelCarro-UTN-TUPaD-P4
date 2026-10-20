import type { Categoria } from "../../types/Categoria";
import { CategoriaCard } from "./CategoriaCard";

type CategoriaListProps = {
  categorias: Categoria[];
  onEdit: (categoria: Categoria) => void;
  onDelete: (id: number) => void;
};

export const CategoriaList = ({
  categorias,
  onEdit,
  onDelete,
}: CategoriaListProps) => {
  if (categorias.length === 0) {
    return (
      <p className="text-slate-400">
        No hay categorías para mostrar.
      </p>
    );
  }

  return (
    <ul className="space-y-2">
      {categorias.map((categoria) => (
        <CategoriaCard
          key={categoria.id}
          categoria={categoria}
          onEdit={onEdit}
          onDelete={onDelete}
        />
      ))}
    </ul>
  );
};