export type Producto = {
  id: number;
  nombre: string;
  descripcion: string | null;
  precio_base: number;
  imagenes_url: string[] | null;
  disponible: boolean;
  categorias: number[];
  created_at: string;   // viene como ISO string
  updated_at: string;   // viene como ISO string
  deleted_at: string | null;
};

export type ProductoPaginatedResponse = {
  total: number;
  items: Producto[];
};