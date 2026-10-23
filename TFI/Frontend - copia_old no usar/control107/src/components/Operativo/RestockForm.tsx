import { useState } from "react";
import { registrarIngreso } from "../../services/operativo";

export default function RestockForm({ turnoId }: { turnoId: number }) {
  const [reposicion, setReposicion] = useState(0);

  const handleSubmit = () => {
    registrarIngreso(turnoId, {
      insumos: [
        { id: 1, cantidad: 0, cantidadRestockeo: reposicion }
      ],
      observaciones: ""
    });
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-2">
        <label className="font-barlow text-petro">Reposición de gasas</label>
        <input
          className="border p-2 rounded font-plex"
          type="number"
          value={reposicion}
          onChange={(e) => setReposicion(Number(e.target.value))}
        />
      </div>

      <button
        className="bg-turquesa text-white px-4 py-2 rounded font-plex"
        onClick={handleSubmit}
      >
        Registrar reposición
      </button>
    </div>
  );
}
