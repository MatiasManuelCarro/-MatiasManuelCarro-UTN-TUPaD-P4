import { useState } from "react";

interface InsumoControl {
  id: number;
  nombre: string;
  categoria: string;
  puntoControl: number;
  esCritico: boolean;
}

interface ControlIngresoProps {
  insumos: InsumoControl[];
}

export default function ControlIngreso({
  insumos,
}: ControlIngresoProps) {
  const [cantidades, setCantidades] = useState<
    Record<number, number>
  >({});

  function actualizarCantidad(
    id: number,
    cantidad: number
  ) {
    setCantidades((prev) => ({
      ...prev,
      [id]: cantidad,
    }));
  }

  const categorias = Array.from(
    new Set(insumos.map((insumo) => insumo.categoria))
  );

  return (
    <div className="space-y-8">
      {categorias.map((categoria) => {
        const insumosCategoria = insumos.filter(
          (insumo) => insumo.categoria === categoria
        );

        return (
          <section key={categoria}>
            <h3 className="mb-3 font-barlow text-lg font-semibold text-petro">
              {categoria}
            </h3>

            <div className="overflow-hidden rounded-xl border border-gray-200 bg-white">
              {insumosCategoria.map((insumo) => {
                const cantidad =
                  cantidades[insumo.id] ?? 0;

                const faltante = Math.max(
                  0,
                  insumo.puntoControl - cantidad
                );

                return (
                  <div
                    key={insumo.id}
                    className="
                      grid grid-cols-[1fr_110px]
                      items-center gap-4
                      border-b border-gray-100
                      p-4 last:border-b-0
                    "
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <p className="font-plex font-semibold text-petro">
                          {insumo.nombre}
                        </p>

                        {insumo.esCritico && (
                          <span
                            className="
                              rounded bg-coral
                              px-2 py-1
                              text-xs font-semibold text-white
                            "
                          >
                            CRÍTICO
                          </span>
                        )}
                      </div>

                      <p className="mt-1 text-sm text-petro/60">
                        Punto de control:{" "}
                        {insumo.puntoControl}
                      </p>

                      {faltante > 0 && (
                        <p className="mt-1 text-sm font-semibold text-coral">
                          Faltan {faltante}
                        </p>
                      )}
                    </div>

                    <div>
                      <label
                        htmlFor={`insumo-${insumo.id}`}
                        className="mb-1 block text-xs text-petro/60"
                      >
                        Cantidad
                      </label>

                      <input
                        id={`insumo-${insumo.id}`}
                        type="number"
                        min="0"
                        value={cantidad}
                        onChange={(e) =>
                          actualizarCantidad(
                            insumo.id,
                            Math.max(
                              0,
                              Number(e.target.value)
                            )
                          )
                        }
                        className="
                          w-full rounded-lg
                          border border-gray-300
                          p-2 text-center
                          font-mono text-lg
                          focus:border-turquesa
                          focus:outline-none
                          focus:ring-2
                          focus:ring-turquesa/20
                        "
                      />
                    </div>
                  </div>
          );
              })}
            </div>
          </section>
        );
      })}
    </div>
  );
}
