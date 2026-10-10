export const getControlInsumos = async (turnoId: number) => {
  const res = await fetch(`http://localhost:8000/control_insumos/${turnoId}`);
  if (!res.ok) throw new Error("Error obteniendo control de insumos");
  return res.json();
};

export const actualizarControl = async (id: number, data: object) => {
  const res = await fetch(`http://localhost:8000/control_insumos/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Error actualizando control");
  return res.json();
};

export const getTurno = async (id: number) => {
  const res = await fetch(`http://localhost:8000/turnos/${id}`);
  if (!res.ok) throw new Error("Error obteniendo turno");
  return res.json();
};

export const actualizarTurno = async (id: number, data: object) => {
  const res = await fetch(`http://localhost:8000/turnos/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Error actualizando turno");
  return res.json();
};
