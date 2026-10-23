import { API_URL } from "./api";
import type { Insumo } from "../interfaces/Insumo";

const BASE = `${API_URL}/insumos`;

export async function listarInsumos(): Promise<Insumo[]> {
  const res = await fetch(BASE);

  if (!res.ok) {
    throw new Error("Error al listar los insumos");
  }

  return res.json();
}