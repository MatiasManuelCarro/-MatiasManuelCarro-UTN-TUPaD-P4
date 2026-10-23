import { API_URL } from "./api";
import type { Ambulancia, AmbulanciaRequest } from "../interfaces/ambulancia";

const BASE = `${API_URL}/ambulancias`;

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
      // Se mantiene el mensaje HTTP.
    }

    throw new Error(mensaje);
  }

  if (res.status === 204) {
    return undefined as T;
  }

  return res.json();
}

export async function listarAmbulancias(): Promise<Ambulancia[]> {
  const res = await fetch(BASE);

  return procesarRespuesta<Ambulancia[]>(res);
}

export async function obtenerAmbulancia(
  id: number
): Promise<Ambulancia> {
  const res = await fetch(`${BASE}/${id}`);

  return procesarRespuesta<Ambulancia>(res);
}

export async function crearAmbulancia(
  data: AmbulanciaRequest
): Promise<Ambulancia> {
  const res = await fetch(BASE, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return procesarRespuesta<Ambulancia>(res);
}

export async function actualizarAmbulancia(
  id: number,
  data: AmbulanciaRequest
): Promise<Ambulancia> {
  const res = await fetch(`${BASE}/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return procesarRespuesta<Ambulancia>(res);
}

export async function eliminarAmbulancia(
  id: number
): Promise<void> {
  const res = await fetch(`${BASE}/${id}`, {
    method: "DELETE",
  });

  return procesarRespuesta<void>(res);
}