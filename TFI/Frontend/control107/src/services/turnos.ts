const BASE = "http://localhost:8000/v1/turnos";

// Listar todos los turnos
export const listarTurnos = async () => {
  const res = await fetch(BASE);
  return res.json();
};

// Obtener un turno por ID
export const getTurno = async (id: number) => {
  const res = await fetch(`${BASE}/${id}`);
  return res.json();
};

// Crear turno
export const crearTurno = async (data: object) => {
  const res = await fetch(BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
};

// Actualizar turno (estado, observaciones, etc.)
export const actualizarTurno = async (id: number, data: object) => {
  const res = await fetch(`${BASE}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
};

// Turnos activos (PROGRAMADO o EN_CURSO)
export const turnosActivos = async () => {
  const res = await fetch(`${BASE}/activos`);
  return res.json();
};

// Iniciar turno (control ingreso)
export const iniciarTurno = async (data: object) => {
  const res = await fetch(`${BASE}/ingreso`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
};

// Finalizar turno (control egreso)
export const finalizarTurno = async (data: object) => {
  const res = await fetch(`${BASE}/egreso`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
};

// Cancelar turno
export const cancelarTurno = async (id: number, observaciones: string) => {
  const res = await fetch(`${BASE}/${id}/cancelar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ observaciones }),
  });
  return res.json();
};
