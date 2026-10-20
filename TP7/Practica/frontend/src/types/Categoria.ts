export type Categoria = {
  id: number;
  nombre: string;
  descripcion: string;
  created_at: string;
  updated_at: string;
};

export type CategoriaCreate = {
  nombre: string;
  descripcion: string;
};

export interface CategoriaUpdate {
  nombre: string;
  descripcion: string;
}

export type CategoriaPaginatedResponse = {
  total: number;
  items: Categoria[];
};