import { listarInsumos } from "../services/insumos";
import type { Insumo } from "../interfaces/Insumo";
import { useEffect, useState } from "react";
import { listarAmbulancias } from "../services/ambulancias";

export default function AdminAmbulancias() {
  const [ambulancias, setAmbulancias] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [insumos, setInsumos] = useState<Insumo[]>([]);

useEffect(() => {
  async function cargarDatos() {
    setLoading(true);
    setError("");

    try {
      const [ambulanciasData, insumosData] = await Promise.all([
        listarAmbulancias(),
        listarInsumos(),
      ]);

      setAmbulancias(ambulanciasData);
      setInsumos(insumosData);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "No se pudieron cargar los datos"
      );
    } finally {
      setLoading(false);
    }
  }

  cargarDatos();
}, []);
  if (loading) {
    return <div className="p-10 text-petro animate-pulse">Cargando ambulancias...</div>;
  }

  if (error) {
    return (
      <div className="p-10">
        <div className="bg-coral text-white p-4 rounded-lg shadow-lg font-plex">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-fondo p-10 font-plex text-petro flex justify-center">
      <div className="w-full max-w-5xl">
        <h1 className="text-4xl font-barlow mb-10 tracking-tight">
          Ambulancias
        </h1>

        {ambulancias.length === 0 && (
          <p className="text-azul">No hay ambulancias registradas.</p>
        )}

        <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {ambulancias.map((a) => (
            <li
              key={a.id}
              className="
                bg-white p-6 rounded-xl shadow-md border border-gray-100
                hover:shadow-xl hover:-translate-y-1 transition-all duration-300
              "
            >
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-2xl font-barlow">
                  Unidad #{a.id}
                </h2>

                <EstadoBadge disponible={a.disponible} />
              </div>

              <p className="text-sm text-petro/80 mb-6">
                Patente: <span className="font-bold text-petro">{a.patente}</span>
              </p>

              <button
                className="
                  bg-turquesa text-white px-5 py-2.5 rounded-lg
                  hover:bg-petro transition-colors duration-300
                  font-barlow shadow-sm
                "
              >
                Ver detalles
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

function EstadoBadge({ disponible }: { disponible: boolean }) {
  const estado = disponible ? "Disponible" : "No disponible";
  const color = disponible ? "bg-verde" : "bg-coral";

  return (
    <span
      className={`
        ${color} text-white px-3 py-1.5 rounded-md font-barlow text-xs
        shadow-sm tracking-wide
      `}
    >
      {estado}
    </span>
  );
}
