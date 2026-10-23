export type HorarioTurno =
  | "MANIANA"
  | "TARDE"
  | "NOCHE";

export type EstadoTurno =
  | "PROGRAMADO"
  | "EN_CURSO"
  | "FINALIZADO"
  | "CANCELADO";

export interface UsuarioTurno {
  id: number;
  email: string;
}

export interface AmbulanciaTurno {
  id: number;
  patente: string;
}

export interface ControlInsumoTurno {
  nombre: string;
  categoria: string;
  esCritico: boolean;
  cantidadIngreso: number;
  cantidadEgreso: number | null;
  ingresoFaltante: number;
  cantidadUsada: number | null;
  cantidadRestockeo: number | null;
}

export interface Turno {
  id: number;
  fecha: string;
  horario: HorarioTurno;
  estado: EstadoTurno;

  chofer: string;
  medico: string;

  ambulancia: AmbulanciaTurno;
  enfermero: UsuarioTurno | null;
  admin: UsuarioTurno | null;

  observacionesIngreso: string | null;
  observacionesEgreso: string | null;

  controlInsumos: ControlInsumoTurno[];
}

export interface TurnoRequest {
  fecha: string;
  horario: HorarioTurno;
  adminId: number;
  enfermeroId: number;
  ambulanciaId: number;
  nombreChofer: string;
  nombreMedico: string;
}