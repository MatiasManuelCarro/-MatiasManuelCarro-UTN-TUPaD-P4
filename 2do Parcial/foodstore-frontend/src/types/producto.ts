import type { Categoria } from "./categoria"
import type { UnidadMedida } from "./unidadMedida"

export interface Producto{
    id: number
    nombre: string
    descripcion: string | null
    precio_base: string
    unidad_venta_id: number
    stock_cantidad: string
    disponible: boolean

    unidad_venta: UnidadMedida
    categorias: Categoria[]
    hay_stock: boolean    
}