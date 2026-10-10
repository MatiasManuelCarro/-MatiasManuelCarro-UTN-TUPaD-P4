export const getTurno = async (id: number) => {
  const res = await fetch(`http://localhost:8000/turnos/${id}`);
  return res.json();
};

export const actualizarTurno = async (id: number, data: object) => {
  const res = await fetch(`http://localhost:8000/turnos/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
};
