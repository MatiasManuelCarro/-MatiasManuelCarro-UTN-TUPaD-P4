import type { Autor } from "../types/autor";
import { AutorCard } from "./AutorCard";

interface Props {
    autores: Autor[];
}

export function AutorList({ autores }: Props) {
    return (
        <ul className="lista">
            {autores.map((autor) => (
                <AutorCard key={autor.id} autor={autor} />
            ))}
        </ul>
    );
}
