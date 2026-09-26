import type { EstadoTurno, Turno } from "../types/turno";

// Props del componente. Siempre se tipan con una interface.
interface TurnoCardProps {
  turno: Turno;
}

// Color de fondo del badge segun el estado del turno.
const coloresEstado: Record<EstadoTurno, string> = {
  pendiente: "bg-amber-100 text-amber-800",
  confirmado: "bg-teal-100 text-teal-800",
  atendido: "bg-slate-200 text-slate-700",
  cancelado: "bg-red-100 text-red-800",
};

// Tarjeta que muestra los datos de un turno. Recibe los datos por props.
function TurnoCard({ turno }: TurnoCardProps) {
  return (
    <article className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-start justify-between gap-2">
        <h3 className="font-semibold text-slate-800">
          {turno.paciente.nombre} {turno.paciente.apellido}
        </h3>
        <span
          className={`rounded-full px-3 py-1 text-xs font-medium ${coloresEstado[turno.estado]}`}
        >
          {turno.estado}
        </span>
      </div>

      <p className="mt-2 text-sm text-slate-600">{turno.motivo}</p>

      <dl className="mt-3 grid grid-cols-2 gap-2 text-sm text-slate-500">
        <div>
          <dt className="font-medium text-slate-700">Fecha</dt>
          <dd>{turno.fecha}</dd>
        </div>
        <div>
          <dt className="font-medium text-slate-700">Hora</dt>
          <dd>{turno.hora}</dd>
        </div>
        <div>
          <dt className="font-medium text-slate-700">Profesional</dt>
          <dd>{turno.profesional}</dd>
        </div>
        <div>
          <dt className="font-medium text-slate-700">DNI</dt>
          <dd>{turno.paciente.dni}</dd>
        </div>
      </dl>
    </article>
  );
}

export default TurnoCard;
