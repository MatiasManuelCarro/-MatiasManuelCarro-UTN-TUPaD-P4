import { API_URL } from "./api";

export const registrarIngreso = async (
  turnoId: number,
  data: object
) => {
  const res = await fetch(`${API_URL}/turnos/ingreso`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ turnoId, ...data }),
  });

  if (!res.ok) {
    throw new Error("Error registrando ingreso");
  }

  return res.json();
};

export const registrarEgreso = async (
  turnoId: number,
  data: object
) => {
  const res = await fetch(`${API_URL}/turnos/egreso`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ turnoId, ...data }),
  });

  if (!res.ok) {
    throw new Error("Error registrando egreso");
  }

  return res.json();
};

export const cancelarTurno = async (
  turnoId: number,
  observaciones: string
) => {
  const res = await fetch(`${API_URL}/turnos/${turnoId}/cancelar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ observaciones }),
  });

  if (!res.ok) {
    throw new Error("Error cancelando turno");
  }

  return res.json();
};