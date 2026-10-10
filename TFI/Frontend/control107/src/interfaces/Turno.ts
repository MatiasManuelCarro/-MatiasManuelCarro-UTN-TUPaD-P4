export interface Turno {
  id: number;
  fecha: string;
  horario: string;
  estado: "PROGRAMADO" | "EN_CURSO" | "FINALIZADO" | "CANCELADO";
  nombre_chofer: string;
  nombre_medico: string;
  ambulancia_id: number;
  enfermero_id: number;
  admin_id: number;
  observaciones_ingreso?: string | null;
  observaciones_egreso?: string | null;
}
