import type { Producto } from "../types/producto";

export default function ProductoCard({ producto }: { producto: Producto }) {
  return (
    <div className="rounded-md border bg-mist-50 p-4 shadow-sm transition-shadow hover:shadow-md">
      <h3 className="text-lg font-semibold">{producto.nombre}</h3>
      <p className="text-sm text-gray-600">{producto.descripcion}</p>
      <p className="mt-2 font-bold text-fuchsia-900">
        ${producto.precio.toFixed(2)}
      </p>
    </div>
  );
}
