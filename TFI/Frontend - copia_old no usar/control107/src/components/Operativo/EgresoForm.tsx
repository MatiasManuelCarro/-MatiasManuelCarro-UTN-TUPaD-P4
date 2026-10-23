import { useState } from "react";
import { registrarEgreso } from "../../services/operativo";

export default function EgresoForm({ turnoId }: { turnoId: number }) {
  const [gasasRestantes, setGasasRestantes] = useState(0);

  const handleSubmit = () => {
    registrarEgreso(turnoId, {
      insumos: [
        { id: 1, cantidad: gasasRestantes }
      ],
      observaciones: ""
    });
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-2">
        <label className="font-barlow text-petro">Gasas restantes</label>
        <input
          className="border p-2 rounded font-plex"
          type="number"
          value={gasasRestantes}
          onChange={(e) => setGasasRestantes(Number(e.target.value))}
        />
      </div>

      <button
        className="bg-turquesa text-white px-4 py-2 rounded font-plex"
        onClick={handleSubmit}
      >
        Registrar egreso
      </button>
    </div>
  );
}
