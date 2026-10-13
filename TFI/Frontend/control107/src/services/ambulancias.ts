export async function listarAmbulancias() {
  const res = await fetch("http://localhost:8000/v1/ambulancias");
  return await res.json();
}
