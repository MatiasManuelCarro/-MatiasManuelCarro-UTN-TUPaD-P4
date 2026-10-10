export interface ControlInsumo {
  id: number;
  turno_id: number;
  insumo_id: number;
  insumo_nombre: string;
  categoria_id: number;
  critico: boolean;
  punto_control: number;
  cantidad_ingreso: number | null;
  cantidad_restockeo: number | null;
  cantidad_egreso: number | null;
  ingreso_faltante: number;
  cantidad_usada: number;
}
