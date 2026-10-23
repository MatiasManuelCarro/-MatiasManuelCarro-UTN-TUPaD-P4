import { API_URL } from "./api";
import type { Turno, TurnoRequest } from "../interfaces/Turno";

const BASE = `${API_URL}/turnos`;

async function procesarRespuesta<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let mensaje = `Error HTTP ${res.status}`;

    try {
      const error = await res.json();

      mensaje =
        error.detalles?.join(", ") ??
        error.message ??
        error.error ??
        mensaje;
    } catch {
      const texto = await res.text();

      if (texto) {
        mensaje = texto;
      }
    }

    throw new Error(mensaje);
  }

  if (res.status === 204) {
    return undefined as T;
  }

  return res.json();
}

export const listarTurnos = async (): Promise<Turno[]> => {
  const res = await fetch(BASE);

  return procesarRespuesta<Turno[]>(res);
};

export const getTurno = async (id: number): Promise<Turno> => {
  const res = await fetch(`${BASE}/${id}`);

  return procesarRespuesta<Turno>(res);
};

export const crearTurno = async (
  data: TurnoRequest
): Promise<Turno> => {
  const res = await fetch(BASE, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return procesarRespuesta<Turno>(res);
};

export const actualizarTurno = async (
  id: number,
  data: Partial<TurnoRequest>
): Promise<Turno> => {
  const res = await fetch(`${BASE}/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return procesarRespuesta<Turno>(res);
};

export const turnosActivos = async (): Promise<Turno[]> => {
  const res = await fetch(`${BASE}/activos`);

  return procesarRespuesta<Turno[]>(res);
};

export const iniciarTurno = async (
  data: object
): Promise<Turno> => {
  const res = await fetch(`${BASE}/ingreso`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return procesarRespuesta<Turno>(res);
};

export const finalizarTurno = async (
  data: object
): Promise<Turno> => {
  const res = await fetch(`${BASE}/egreso`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return procesarRespuesta<Turno>(res);
};

export const cancelarTurno = async (
  id: number,
  observaciones: string
): Promise<Turno> => {
  const res = await fetch(`${BASE}/${id}/cancelar`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ observaciones }),
  });

  return procesarRespuesta<Turno>(res);
};
