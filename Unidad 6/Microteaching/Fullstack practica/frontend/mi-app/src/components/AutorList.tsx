import type { Autor } from "../types/autor";

export function AutorList({ autores }: { autores: Autor[] }) {
    return (
        <ul>
            {autores.map((autor) => (
                <li key={autor.id}>
                    {autor.nombre} — {autor.libros?.length ?? 0} libros
                </li>
            ))}
        </ul>
    );
}
