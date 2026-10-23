import { useEffect, useState } from "react";
import { BtnPrimary } from "../components/Base/BtnPrimary";
import { BtnSecondary } from "../components/Base/BtnSecondary";
import { Panel } from "../components/Panel";
import IngresoForm from "../components/Operativo/IngresoForm";
import RestockForm from "../components/Operativo/RestockForm";
import EgresoForm from "../components/Operativo/EgresoForm";
import ObservacionesForm from "../components/Operativo/ObservacionesForm";

export default function OperativoEnfermero() {
  const [turnoId, setTurnoId] = useState<number | null>(null);

  useEffect(() => {
    fetch("http://localhost:8000/v1/turnos/activos")
      .then((res) => res.json())
      .then((turnos) => {
        console.log("TURNOS ACTIVOS:", turnos); // debug mínimo

        if (turnos.length > 0) {
          setTurnoId(turnos[0].id);
        } else {
          // fallback quirúrgico
          setTurnoId(1);
        }
      })
      .catch(() => {
        // fallback si el backend falla
        setTurnoId(1);
      });
  }, []);


  if (!turnoId) {
    return (
      <div className="min-h-screen bg-fondo p-6 max-w-4xl mx-auto">
        <h1 className="font-barlow text-3xl text-petro">Mi turno</h1>
        <p className="font-plex mt-4">Cargando turno...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-fondo p-6 space-y-6 max-w-4xl mx-auto">

      <h1 className="font-barlow text-3xl text-petro">Mi turno</h1>

      <Panel title="Control de ingreso">
        <IngresoForm turnoId={turnoId} />
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
        <BtnPrimary>Finalizar turno</BtnPrimary>
        <BtnSecondary>Cancelar turno</BtnSecondary>
      </div>
    </div>
  );
}
