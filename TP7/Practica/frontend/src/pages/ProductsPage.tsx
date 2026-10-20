import { useQuery } from "@tanstack/react-query";
import { getProducts } from "../services/Productos";
import type { Producto, ProductoPaginatedResponse } from "../types/Producto";


function ProductsPage() {
  const { data, isLoading, isError } = useQuery<ProductoPaginatedResponse>({
    queryKey: ["productos"],
    queryFn: getProducts,
  });

  if (isLoading) return <p>Cargando...</p>;
  if (isError) return <p>Error al cargar productos</p>;
  if (!data || data.items.length === 0) {
    return <p>No hay productos para mostrar</p>;
  }

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Productos</h1>
      <ul className="space-y-2">
        {data.items.map((prod: Producto) => (
          <li key={prod.id} className="rounded bg-slate-800 p-3 transition-all duration-200 hover:bg-slate-700 hover:shadow-lg hover:-translate-y-0.5">
            <p className="font-semibold">{prod.nombre}</p>
            <p className="text-sm text-slate-300">{prod.descripcion}</p>
            <p className="text-sm">Precio: ${prod.precio_base}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProductsPage;
