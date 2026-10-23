import { registrarIngreso } from "../../services/operativo";
import { useState } from "react";

export default function IngresoForm({ turnoId }: { turnoId: number }) {
  const [gasas, setGasas] = useState(0);
  const [oxigeno, setOxigeno] = useState(0);

  const handleSubmit = () => {
    registrarIngreso(turnoId, {
      insumos: [
        { id: 1, cantidad: gasas, cantidadRestockeo: 0 },
        { id: 3, cantidad: oxigeno, cantidadRestockeo: 0 }
      ],
      observaciones: ""
    });
  };

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-2">
        <label className="font-barlow text-petro">Gasas</label>
        <input
          className="border p-2 rounded font-plex"
          type="number"
          value={gasas}
          onChange={(e) => setGasas(Number(e.target.value))}
        />
      </div>

      <div className="flex flex-col gap-2">
        <label className="font-barlow text-petro">Oxígeno (psi)</label>
        <input
          className="border p-2 rounded font-mono"
          type="number"
          value={oxigeno}
          onChange={(e) => setOxigeno(Number(e.target.value))}
        />
      </div>

      <button
        className="bg-turquesa text-white px-4 py-2 rounded font-plex"
        onClick={handleSubmit}
      >
        Registrar ingreso
      </button>
    </div>
  );
}
