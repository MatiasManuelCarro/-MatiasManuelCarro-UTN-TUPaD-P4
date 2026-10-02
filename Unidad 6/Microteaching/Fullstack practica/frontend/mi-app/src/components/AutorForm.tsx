import { useState } from "react";
import { crearAutor } from "../services/api";

export function AutorForm({ onCreated }: { onCreated: () => void }) {
    const [nombre, setNombre] = useState("");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        await crearAutor(nombre);
        setNombre("");
        onCreated();
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                placeholder="Nombre del autor"
            />
            <button type="submit">Crear</button>
        </form>
    );
}
