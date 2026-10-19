import { useQuery } from "@tanstack/react-query";
import { getProducts } from "../api/Productos";
import type { ProductoPaginatedResponse } from "../types/Producto";

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
        {data.items.map((prod: any) => (
          <li key={prod.id} className="p-3 bg-slate-800 rounded">
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
