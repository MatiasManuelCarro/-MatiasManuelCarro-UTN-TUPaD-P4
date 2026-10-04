import { useState } from "react";
import type { Categoria } from "../types/categoria";

interface Props {
    abierta: boolean;
    categoria: Categoria | null;
    onClose: () => void;
    onSubmit: (data: { nombre: string; descripcion: string }) => void;
}

export default function CategoriaModal({ abierta, categoria, onClose, onSubmit }: Props) {
    if (!abierta) return null;

    const [nombre, setNombre] = useState(categoria?.nombre ?? "");
    const [descripcion, setDescripcion] = useState(categoria?.descripcion ?? "");

    function handleSubmit() {
        onSubmit({ nombre, descripcion });
        onClose();
    }

    return (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center">
            <div className="bg-white p-6 rounded shadow w-80">
                <h2 className="text-lg font-bold mb-4">
                    {categoria ? "Editar Categoría" : "Nueva Categoría"}
                </h2>

                <input
                    className="border p-2 w-full mb-2"
                    placeholder="Nombre"
                    value={nombre}
                    onChange={(e) => setNombre(e.target.value)}
                />

                <input
                    className="border p-2 w-full mb-4"
                    placeholder="Descripción"
                    value={descripcion}
                    onChange={(e) => setDescripcion(e.target.value)}
                />

                <div className="flex justify-end gap-2">
                    <button className="px-3 py-1 bg-gray-300 rounded" onClick={onClose}>
                        Cancelar
                    </button>

                    <button className="px-3 py-1 bg-mist-600 text-white rounded" onClick={handleSubmit}>
                        Guardar
                    </button>
                </div>
            </div>
        </div>
    );
}
