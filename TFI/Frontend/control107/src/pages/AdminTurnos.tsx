// src/pages/AdminTurnos.tsx
import { Panel } from "../components/Panel";
import { BtnPrimary } from "../components/Base/BtnPrimary";

export default function AdminTurnos() {
  return (
    <div className="p-6 space-y-6 bg-fondo min-h-screen">
      <h1 className="font-barlow text-3xl text-petro">Turnos</h1>

      <Panel title="Programación">
        <div className="space-y-4">
          <div className="p-4 bg-blanco border rounded flex justify-between">
            <span className="font-plex text-petro">09/10/2026 – Mañana</span>
            <span className="font-mono text-azul">Programado</span>
          </div>
        </div>
      </Panel>

      <BtnPrimary>Crear turno</BtnPrimary>
    </div>
  );
}
