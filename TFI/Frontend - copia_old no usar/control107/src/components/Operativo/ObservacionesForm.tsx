import { cancelarTurno } from "../../services/operativo";
import { useState } from "react";

export default function ObservacionesForm({ turnoId }: { turnoId: number }) {
  const [obs, setObs] = useState("");

  const handleSubmit = () => {
    cancelarTurno(turnoId, obs);
  };

  return (
    <div className="space-y-4">
      <textarea
        className="border p-3 rounded w-full font-plex"
        rows={4}
        placeholder="Registrar observaciones..."
        value={obs}
        onChange={(e) => setObs(e.target.value)}
      />

      <button
        className="bg-turquesa text-white px-4 py-2 rounded font-plex"
        onClick={handleSubmit}
      >
        Guardar observaciones
      </button>
    </div>
  );
}
