import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const getAutores = async () => {
  const res = await api.get("/autores");
  return res.data;
};

export const crearAutor = async (nombre: string) => {
  const res = await api.post("/autores", { nombre });
  return res.data;
};

export const crearLibro = async (titulo: string, autor_id: number) => {
  const res = await api.post("/libros", { titulo, autor_id });
  return res.data;
};
