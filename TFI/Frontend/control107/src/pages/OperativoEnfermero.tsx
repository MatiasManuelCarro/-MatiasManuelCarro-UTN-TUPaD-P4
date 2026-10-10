// src/pages/OperativoEnfermero.tsx
import { BtnPrimary } from "../components/Base/BtnPrimary";
import { BtnSecondary } from "../components/Base/BtnSecondary";
import { Panel } from "../components/Panel";
import IngresoForm from "../components/Operativo/IngresoForm";
import RestockForm from "../components/Operativo/RestockForm";
import EgresoForm from "../components/Operativo/EgresoForm";
import ObservacionesForm from "../components/Operativo/ObservacionesForm";
export default function OperativoEnfermero() {
  return (
    <div className="min-h-screen bg-fondo p-6 space-y-6 max-w-4xl mx-auto">

      <h1 className="font-barlow text-3xl text-petro">Mi turno</h1>

      <Panel title="Control de ingreso">
        <IngresoForm />
      </Panel>

      <Panel title="Reposiciones">
        <RestockForm />
      </Panel>

      <Panel title="Control de egreso">
        <EgresoForm />
      </Panel>

      <Panel title="Observaciones">
        <ObservacionesForm />
      </Panel>

      <div className="flex gap-4">
        <BtnPrimary>Finalizar turno</BtnPrimary>
        <BtnSecondary>Cancelar turno</BtnSecondary>
      </div>
    </div>
  );
}
