import { API_URL } from "./api";
import type {
  CrearUsuarioRequest,
  EditarUsuarioRequest,
  Usuario,
} from "../interfaces/Usuario";

const BASE = `${API_URL}/usuarios`;

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
      // Se conserva el mensaje HTTP si la respuesta no contiene JSON.
    }

    throw new Error(mensaje);
  }

  if (res.status === 204) {
    return undefined as T;
  }

  return res.json();
}

export async function listarUsuarios(): Promise<Usuario[]> {
  const res = await fetch(BASE);

  return procesarRespuesta<Usuario[]>(res);
}

export async function obtenerUsuario(
  id: number
): Promise<Usuario> {
  const res = await fetch(`${BASE}/${id}`);

  return procesarRespuesta<Usuario>(res);
}

export async function crearUsuario(
  data: CrearUsuarioRequest
): Promise<Usuario> {
  const res = await fetch(BASE, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return procesarRespuesta<Usuario>(res);
}

export async function actualizarUsuario(
  id: number,
  data: EditarUsuarioRequest
): Promise<Usuario> {
  const res = await fetch(`${BASE}/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  return procesarRespuesta<Usuario>(res);
}

export async function eliminarUsuario(
  id: number
): Promise<void> {
  const res = await fetch(`${BASE}/${id}`, {
    method: "DELETE",
  });

  return procesarRespuesta<void>(res);
}