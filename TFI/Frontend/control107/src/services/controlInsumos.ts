export const getControlInsumos = async (turnoId: number) => {
  const res = await fetch(`http://localhost:8000/control_insumos/${turnoId}`);
  return res.json();
};

export const actualizarControl = async (id: number, data: object) => {
  const res = await fetch(`http://localhost:8000/control_insumos/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
};
