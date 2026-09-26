// Tipos del dominio. Reflejan los campos que expone el backend de la Parte A.

/** Datos del paciente que se muestran junto al turno. */
export interface Paciente {
  id: number
  nombre: string
  apellido: string
  dni: string
  telefono: string
}

/** Estados posibles de un turno. Un union type evita strings invalidos. */
export type EstadoTurno = 'pendiente' | 'confirmado' | 'atendido' | 'cancelado'

/** Turno del consultorio, con el paciente al que pertenece. */
export interface Turno {
  id: number
  fecha: string
  hora: string
  profesional: string
  motivo: string
  estado: EstadoTurno
  paciente: Paciente
}
