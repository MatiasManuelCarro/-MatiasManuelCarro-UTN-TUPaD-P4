export const registrarIngreso = async (turnoId: number, data: object) => {
  const res = await fetch(`http://localhost:8000/v1/turnos/ingreso`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ turnoId, ...data }),
  });
  return res.json();
};

export const registrarEgreso = async (turnoId: number, data: object) => {
  const res = await fetch(`http://localhost:8000/v1/turnos/egreso`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ turnoId, ...data }),
  });
  return res.json();
};

export const cancelarTurno = async (turnoId: number, observaciones: string) => {
  const res = await fetch(`http://localhost:8000/v1/turnos/${turnoId}/cancelar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ observaciones }),
  });
  return res.json();
};
