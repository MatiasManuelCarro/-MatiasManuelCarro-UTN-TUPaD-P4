export interface Insumo {
  id: number;
  nombre: string;
  categoriaId: number;
  categoria?: string;
  puntoControl: number;
  esCritico: boolean;
}
