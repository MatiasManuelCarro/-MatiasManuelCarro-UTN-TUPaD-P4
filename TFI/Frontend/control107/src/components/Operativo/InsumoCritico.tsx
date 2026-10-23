export type NivelCritico =
  | "OK"
  | "ALERTA"
  | "CAMBIAR";

interface InsumoCriticoProps {
  id: number;
  nombre: string;
  categoria: string;

  // Umbral mínimo operativo.
  puntoControl: number;

  // Valor que representa el 100% de la barra.
  capacidadMaxima: number;

  // Por ejemplo: "bar".
  unidad: string;

  // Valor introducido por el enfermero.
  cantidad: number;

  onCantidadChange: (
    id: number,
    cantidad: number
  ) => void;
}

function calcularNivelCritico(
  cantidad: number,
  puntoControl: number
): NivelCritico {
  if (cantidad <= puntoControl * 0.5) {
    return "CAMBIAR";
  }

  if (cantidad <= puntoControl) {
    return "ALERTA";
  }

  return "OK";
}

function obtenerEstiloNivel(nivel: NivelCritico) {
  switch (nivel) {
    case "OK":
      return {
        texto: "Nivel correcto",
        fondo: "bg-verde/10",
        borde: "border-verde",
        badge: "bg-verde",
        barra: "bg-verde",
      };

    case "ALERTA":
      return {
        texto: "Nivel de alerta",
        fondo: "bg-ambar/10",
        borde: "border-ambar",
        badge: "bg-ambar",
        barra: "bg-ambar",
      };

    case "CAMBIAR":
      return {
        texto: "Cambiar o reponer",
        fondo: "bg-coral/10",
        borde: "border-coral",
        badge: "bg-coral",
        barra: "bg-coral",
      };
  }
}

export default function InsumoCritico({
  id,
  nombre,
  categoria,
  puntoControl,
  capacidadMaxima,
  unidad,
  cantidad,
  onCantidadChange,
}: InsumoCriticoProps) {
  const nivel = calcularNivelCritico(
    cantidad,
    puntoControl
  );

  const estilos = obtenerEstiloNivel(nivel);

  /*
   * El porcentaje se calcula usando capacidadMaxima.
   *
   * Ejemplo:
   * cantidad = 150
   * capacidadMaxima = 200
   *
   * porcentaje = 75%
   */
  const porcentaje =
    capacidadMaxima > 0
      ? Math.min(
          100,
          Math.max(
            0,
            Math.round(
              (cantidad / capacidadMaxima) * 100
            )
          )
        )
      : 0;

  /*
   * El faltante continúa calculándose
   * contra el punto de control.
   */
  const faltante = Math.max(
    0,
    puntoControl - cantidad
  );

  function handleCantidadChange(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const valor = Number(event.target.value);

    /*
     * Impide cantidades menores que cero
     * o mayores que la capacidad máxima.
     */
    const cantidadValida = Math.min(
      capacidadMaxima,
      Math.max(0, valor)
    );

    onCantidadChange(id, cantidadValida);
  }

  return (
    <article
      className={`
        rounded-xl border-2 p-5
        ${estilos.fondo}
        ${estilos.borde}
      `}
    >
      <div className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
        <div className="flex-1">
          <div className="mb-2 flex flex-wrap items-center gap-2">
            <span
              className={`
                rounded-md px-2.5 py-1
                text-xs font-bold text-white
                ${estilos.badge}
              `}
            >
              {nivel}
            </span>

            <span className="text-xs font-semibold uppercase tracking-wide text-petro/60">
              Insumo crítico
            </span>
          </div>

          <h3 className="font-barlow text-xl text-petro">
            {nombre}
          </h3>

          <p className="mt-1 text-sm text-petro/60">
            {categoria}
          </p>

          <div className="mt-4">
            <div className="mb-2 flex flex-col gap-1 text-sm sm:flex-row sm:justify-between">
              <span className="font-semibold text-petro">
                {estilos.texto}
              </span>

              <span className="font-mono text-petro/70">
                {cantidad} {unidad} de{" "}
                {capacidadMaxima} {unidad}
                {" · "}
                {porcentaje}%
              </span>
            </div>

            <div className="h-3 overflow-hidden rounded-full bg-gray-200">
              <div
                className={`
                  h-full rounded-full transition-all
                  ${estilos.barra}
                `}
                style={{
                  width: `${porcentaje}%`,
                }}
              />
            </div>
          </div>

          <div className="mt-4 grid grid-cols-1 gap-3 text-sm sm:grid-cols-3">
            <div className="rounded-lg bg-white/70 p-3">
              <p className="text-petro/60">
                Capacidad máxima
              </p>

              <p className="mt-1 font-mono text-lg font-semibold text-petro">
                {capacidadMaxima} {unidad}
              </p>
            </div>

            <div className="rounded-lg bg-white/70 p-3">
              <p className="text-petro/60">
                Punto de control
              </p>

              <p className="mt-1 font-mono text-lg font-semibold text-petro">
                {puntoControl} {unidad}
              </p>
            </div>

            <div className="rounded-lg bg-white/70 p-3">
              <p className="text-petro/60">
                Faltante
              </p>

              <p
                className={`
                  mt-1 font-mono text-lg font-semibold
                  ${
                    faltante > 0
                      ? "text-coral"
                      : "text-verde"
                  }
                `}
              >
                {faltante} {unidad}
              </p>
            </div>
          </div>
        </div>

        <label className="flex w-full flex-col gap-2 sm:w-44">
          <span className="text-sm font-semibold text-petro">
            Presión actual
          </span>

          <div className="relative">
            <input
              type="number"
              min={0}
              max={capacidadMaxima}
              step={1}
              value={cantidad}
              onChange={handleCantidadChange}
              className="
                w-full rounded-lg border-2
                border-gray-300 bg-white
                p-3 pr-14 text-center
                font-mono text-xl
                focus:border-turquesa
                focus:outline-none
                focus:ring-2
                focus:ring-turquesa/20
              "
            />

            <span className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 font-mono text-sm text-petro/50">
              {unidad}
            </span>
          </div>

          <span className="text-center text-xs text-petro/50">
            Máximo: {capacidadMaxima} {unidad}
          </span>
        </label>
      </div>
    </article>
  );
}