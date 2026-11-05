import { ProductoCard } from "./ProductoCard";
import type { Producto } from "../types/producto";

interface ProductoListProps {
    productos: Producto[];
    // onEditar: (producto: Producto) => void;
    onDisponibilidad: (producto: Producto) => void;
    // onAnular: (producto: Producto) => void;
}

export function ProductoList({
    productos,
    // onEditar,
    onDisponibilidad,
    // onAnular,
}: ProductoListProps) {
    return (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {productos.map((producto) => (
                <ProductoCard
                    key={producto.id}
                    producto={producto}
                    // onEditar={onEditar}
                    onDisponibilidad={onDisponibilidad}
                    // onAnular={onAnular}
                />
            ))}
        </div>
    );
}
