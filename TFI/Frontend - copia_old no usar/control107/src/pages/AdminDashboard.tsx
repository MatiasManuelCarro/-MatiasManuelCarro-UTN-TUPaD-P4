// src/pages/AdminDashboard.tsx
import { Panel } from "../components/Panel";
export default function AdminDashboard() {
  return (
    <div className="p-6 space-y-6 bg-fondo min-h-screen">
      <h1 className="font-barlow text-3xl text-petro">Dashboard</h1>

      <Panel title="Estado de la flota">
        <div className="grid grid-cols-3 gap-4">
          <div className="p-4 bg-verde text-white rounded font-plex">
            4 móviles disponibles
          </div>
          <div className="p-4 bg-ambar text-white rounded font-plex">
            1 móvil requiere revisión
          </div>
          <div className="p-4 bg-coral text-white rounded font-plex">
            1 móvil crítico
          </div>
        </div>
      </Panel>

      <Panel title="Consumo de insumos">
        <p className="font-mono text-petro">Gasas: 120</p>
        <p className="font-mono text-petro">Oxígeno: 3 tubos</p>
      </Panel>
    </div>
  );
}
