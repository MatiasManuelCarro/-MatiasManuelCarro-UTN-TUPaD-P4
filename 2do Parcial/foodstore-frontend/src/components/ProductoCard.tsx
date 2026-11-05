import type { Producto } from "../types/producto";
// import { actualizarProducto, getProductos, getUnidades } from "../api";

// interface ProductoCardProps {
//     producto: Producto;
//     onEditar: (producto: Producto) => void;
//     onDisponibilidad: (producto: Producto) => void;
//     onAnular: (producto: Producto) => void;
// }

interface ProductoCardProps {
    producto: Producto
    onDisponibilidad: (producto: Producto) => void
    onAnular: (producto: Producto) => void
}

export function ProductoCard({
    producto,
    // onEditar,
    onDisponibilidad,
    onAnular,
}: ProductoCardProps) {
    return (
        <article className="flex flex-col gap-4 rounded-lg border border-gray-200 bg-white p-6">
            <div className="flex items-start justify-between gap-4">
                <div>
                    <h3 className="text-xl font-semibold text-gray-900">
                        {producto.nombre}
                    </h3>

                    <p className="mt-1 text-sm text-gray-600">
                        {producto.descripcion ?? "Sin descripción"}
                    </p>
                </div>

                <span
                    className={
                        producto.disponible
                            ? "rounded-full bg-green-100 px-3 py-1 text-xs font-medium text-green-700"
                            : "rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-600 "
                    }
                >
                    {producto.disponible ? "Disponible" : "No disponible"}
                </span>
            </div>

            <div className="grid gap-2 text-sm text-gray-700">
                <p>
                    <span className="font-medium">stock:</span> {producto.stock_cantidad}{" "}
                    {producto.unidad_venta.simbolo}
                </p>
            </div>

            <div>
                <span
                    className={
                        producto.hay_stock
                            ? "text-sm font-medium text-green-700"
                            : "text-sm font-medium text-red-600"
                    }
                >
                    {producto.hay_stock ? "Con Stock" : "Sin Stock"}
                </span>
            </div>

            {/* Botones */}

            <div className="my-auto flex flex-wrap gap-2 pt-2">
                <button
                    type="button"
                    onClick={() => onDisponibilidad(producto)}
                    className="rounded-lg bg-gray-200 px-4 py-2 text-sm font-medium text-gray-800 hover:bg-gray-300"
                >
                    Disponibilidad
                </button>
                <button
                    type="button"
                    onClick={() => onAnular(producto)}
                    className="rounded-lg bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700"
                >
                    Anular
                </button>
            </div>
        </article>
    );
}
