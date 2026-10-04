import { useState } from "react";

interface Props {
    onAgregar: (nombre:string) => void
}

export function AutorForm({onAgregar}: Props) {
    const [nombre, setNombre] = useState("");

    function enviar(e: React.FormEvent){
        e.preventDefault()
        onAgregar(nombre)
        setNombre('')
    }

    return (
        <form onSubmit={enviar}>
            <input
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                placeholder="Nombre del autor"
            />
            <button>Agregar</button>
        </form>
    );
}
