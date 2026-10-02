import type { Libro } from "./libro";

export interface Autor {
  id: number;
  nombre: string;
  libros?: Libro[];
}
