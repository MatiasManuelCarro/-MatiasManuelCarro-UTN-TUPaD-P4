// Formulario de alta de turno. Solo maquetado: no guarda ni valida nada.
function TurnoForm() {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold text-slate-800">Nuevo turno</h2>

      <form className="grid gap-4 sm:grid-cols-2">
        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-slate-600">Paciente</label>
          <input
            type="text"
            placeholder="Ej: Ana Gomez"
            className="rounded border border-slate-300 px-3 py-2 text-sm"
          />
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-slate-600">Profesional</label>
          <input
            type="text"
            placeholder="Ej: Dr. Perez"
            className="rounded border border-slate-300 px-3 py-2 text-sm"
          />
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-slate-600">Fecha</label>
          <input
            type="date"
            className="rounded border border-slate-300 px-3 py-2 text-sm"
          />
        </div>

        <div className="flex flex-col gap-1">
          <label className="text-sm font-medium text-slate-600">Hora</label>
          <input
            type="time"
            className="rounded border border-slate-300 px-3 py-2 text-sm"
          />
        </div>

        <div className="flex flex-col gap-1 sm:col-span-2">
          <label className="text-sm font-medium text-slate-600">Motivo</label>
          <input
            type="text"
            placeholder="Ej: Control anual"
            className="rounded border border-slate-300 px-3 py-2 text-sm"
          />
        </div>

        <button
          type="button"
          className="rounded bg-teal-700 px-4 py-2 text-sm font-medium text-white sm:col-span-2"
        >
          Guardar turno
        </button>
      </form>
    </section>
  )
}

export default TurnoForm
