import { useEffect, useState } from "react";
import { BtnPrimary } from "../components/Base/BtnPrimary";
import { BtnSecondary } from "../components/Base/BtnSecondary";
import { Panel } from "../components/Panel";
import ControlIngreso from "../components/Operativo/ControlIngreso";
import RestockForm from "../components/Operativo/RestockForm";
import EgresoForm from "../components/Operativo/EgresoForm";
import ObservacionesForm from "../components/Operativo/ObservacionesForm";
import { API_URL } from "../services/api";

const insumosPrueba = [
  {
    id: 1,
    nombre: "Adrenalina 1mg",
    categoria: "FARMACOLOGICOS",
    puntoControl: 20,
    esCritico: false,
  },
  {
    id: 2,
    nombre: "Atropina 1mg",
    categoria: "FARMACOLOGICOS",
    puntoControl: 5,
    esCritico: false,
  },
  {
    id: 3,
    nombre: "Gasas Estériles",
    categoria: "CURACION",
    puntoControl: 30,
    esCritico: false,
  },
  {
    id: 4,
    nombre: "Tubo grande de oxígeno",
    categoria: "OXIGENO",
    puntoControl: 60,
    capacidadMaxima: 200,
    unidad: "bar",
    esCritico: true,
  },
];

export default function OperativoEnfermero() {
  const [turnoId, setTurnoId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API_URL}/turnos/activos`)
      .then((res) => {
        if (!res.ok) {
          throw new Error("Error al obtener los turnos activos");
        }

        return res.json();
      })
      .then((turnos) => {
        console.log("TURNOS ACTIVOS:", turnos);

        if (Array.isArray(turnos) && turnos.length > 0) {
          setTurnoId(turnos[0].id);
        } else {
          setTurnoId(null);
        }
      })
      .catch((error) => {
        console.error("ERROR AL CARGAR TURNO:", error);
        setTurnoId(null);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-fondo p-6 max-w-4xl mx-auto">
        <h1 className="font-barlow text-3xl text-petro">
          Mi turno
        </h1>

        <p className="font-plex mt-4">
          Cargando turno...
        </p>
      </div>
    );
  }

  if (!turnoId) {
    return (
      <div className="min-h-screen bg-fondo p-6 max-w-4xl mx-auto">
        <h1 className="font-barlow text-3xl text-petro">
          Mi turno
        </h1>

        <p className="font-plex mt-4">
          No hay un turno activo.
        </p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-fondo p-6">
      <div className="mx-auto max-w-4xl space-y-6">

        <div>
          <h1 className="font-barlow text-3xl text-petro">
            Mi turno
          </h1>

          <p className="font-plex text-sm text-petro/60 mt-1">
            Turno #{turnoId}
          </p>
        </div>

        {/* BORRADOR DEL NUEVO CONTROL DE INGRESO */}
        <Panel title="Control de ingreso">
          <ControlIngreso insumos={insumosPrueba} />
        </Panel>

        <Panel title="Reposiciones">
          <RestockForm turnoId={turnoId} />
        </Panel>

        <Panel title="Control de egreso">
          <EgresoForm turnoId={turnoId} />
        </Panel>

        <Panel title="Observaciones">
          <ObservacionesForm turnoId={turnoId} />
        </Panel>

        <div className="flex gap-4">
          <BtnPrimary>
            Finalizar turno
          </BtnPrimary>

          <BtnSecondary>
            Cancelar turno
          </BtnSecondary>
        </div>

      </div>
    </div>
  );
}