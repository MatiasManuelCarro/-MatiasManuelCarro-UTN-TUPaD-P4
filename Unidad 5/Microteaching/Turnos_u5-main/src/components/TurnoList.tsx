import type { Turno } from "../types/turno";
import TurnoCard from "./TurnoCard";

interface TurnoListProps {
  turnos: Turno[];
}

// Recibe un array de turnos y renderiza una TurnoCard por cada uno.
function TurnoList({ turnos }: TurnoListProps) {
  return (
    <section>
      <h2 className="mb-4 text-lg font-semibold text-slate-800">
        Turnos ({turnos.length})
      </h2>

      <div className="grid gap-4 sm:grid-cols-2">
        {turnos.map((turno) => (
          <TurnoCard key={turno.id} turno={turno} />
        ))}
      </div>
    </section>
  );
}

export default TurnoList;
