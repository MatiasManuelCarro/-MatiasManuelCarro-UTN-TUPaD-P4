import type { Producto } from "../types/producto"
import ProductoCard from "./ProductoCard"

export default function ProductoList({ productos }: { productos: Producto[] }) {
  return (
    <div className="flex flex-col gap-4">
      {productos.map((p) => (
        <ProductoCard key={p.id} producto={p} />
      ))}
    </div>
  )
}
