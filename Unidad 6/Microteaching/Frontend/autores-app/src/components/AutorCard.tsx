import type { Autor } from "../types/autor";

interface Props {
    autor: Autor;
}

export function AutorCard({ autor }: Props) {
    return (
        <li className="card">
            <span>
                <strong>{autor.nombre}</strong>
            </span>
        </li>
    );
}
