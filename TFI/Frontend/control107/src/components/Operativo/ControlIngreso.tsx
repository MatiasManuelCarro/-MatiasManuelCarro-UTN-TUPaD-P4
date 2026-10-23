import { useState } from "react";
import InsumoCritico from "./InsumoCritico";

export interface InsumoControl {
  id: number;
  nombre: string;
  categoria: string;
  puntoControl: number;
  esCritico: boolean;

  // Temporales para probar el manejo de tubos de oxígeno.
  capacidadMaxima?: number;
  unidad?: string;
}

interface ControlIngresoProps {
  insumos: InsumoControl[];
}

export default function ControlIngreso({
  insumos,
}: ControlIngresoProps) {
  const [cantidades, setCantidades] = useState<Record<number, number>>(
    () =>
      Object.fromEntries(
        insumos.map((insumo) => [
          insumo.id,
          insumo.capacidadMaxima ?? insumo.puntoControl,
        ])
      )
  );

  function actualizarCantidad(
    id: number,
    cantidad: number
  ) {
    setCantidades((prev) => ({
      ...prev,
      [id]: cantidad,
    }));
  }

  // Los insumos críticos se muestran primero.
  const insumosCriticos = insumos.filter(
    (insumo) => insumo.esCritico
  );

  // El resto se muestra después, agrupado por categoría.
  const insumosNormales = insumos.filter(
    (insumo) => !insumo.esCritico
  );

  const categoriasNormales = Array.from(
    new Set(
      insumosNormales.map(
        (insumo) => insumo.categoria
      )
    )
  );

  return (
    <div className="space-y-10">

      {/* INSUMOS CRÍTICOS */}
      {insumosCriticos.length > 0 && (
        <section>
          <div className="mb-4">
            <h2 className="font-barlow text-2xl text-petro">
              Control prioritario
            </h2>

            <p className="mt-1 text-sm text-petro/60">
              Verifica primero los insumos que pueden afectar
              la operatividad de la ambulancia.
            </p>
          </div>

          <div className="space-y-4">
            {insumosCriticos.map((insumo) => (
              <InsumoCritico
                key={insumo.id}
                id={insumo.id}
                nombre={insumo.nombre}
                categoria={insumo.categoria}
                puntoControl={insumo.puntoControl}
                capacidadMaxima={
                  insumo.capacidadMaxima ??
                  insumo.puntoControl
                }
                unidad={insumo.unidad ?? "unidades"}
                cantidad={cantidades[insumo.id] ?? 0}
                onCantidadChange={actualizarCantidad}
              />
            ))}
          </div>
        </section>
      )}

      {/* INSUMOS NORMALES */}
      {insumosNormales.length > 0 && (
        <section>
          <div className="mb-4">
            <h2 className="font-barlow text-2xl text-petro">
              Resto de insumos
            </h2>

            <p className="mt-1 text-sm text-petro/60">
              Registra la cantidad encontrada al comenzar
              el turno.
            </p>
          </div>

          <div className="space-y-8">
            {categoriasNormales.map((categoria) => {
              const insumosCategoria =
                insumosNormales.filter(
                  (insumo) =>
                    insumo.categoria === categoria
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
                            grid items-center gap-4
                            border-b border-gray-100
                            p-4 last:border-b-0
                            sm:grid-cols-[1fr_120px]
                          "
                  >
                          <div>
                            <p className="font-plex font-semibold text-petro">
                              {insumo.nombre}
                            </p>

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

                          <label className="flex flex-col gap-1">
                            <span className="text-xs text-petro/60">
                              Cantidad
                            </span>

                            <input
                              type="number"
                              min={0}
                              value={cantidad}
                              onChange={(event) => {
                                const valor = Math.max(
                                  0,
                                  Number(event.target.value)
                                );

                                actualizarCantidad(
                                  insumo.id,
                                  valor
                                );
                              }}
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
                          </label>
                        </div>
                      );
                    })}
                  </div>
                </section>
              );
            })}
          </div>
        </section>
      )}

    </div>
  );
}