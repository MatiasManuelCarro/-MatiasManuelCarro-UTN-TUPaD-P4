export interface Turno {
  id: number;
  fecha: string;
  horario: string;
  estado: "PROGRAMADO" | "EN_CURSO" | "FINALIZADO" | "CANCELADO";

  chofer: string;
  medico: string;

  ambulancia: { id: number };
  enfermero: { id: number };
  admin: { id: number };

  observacionesIngreso?: string | null;
  observacionesEgreso?: string | null;
}
