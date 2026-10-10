// src/pages/AdminHistorial.tsx
import { Panel } from "../components/Panel";

export default function AdminHistorial() {
  return (
    <div className="p-6 space-y-6 bg-fondo min-h-screen">
      <h1 className="font-barlow text-3xl text-petro">Historial Operativo</h1>

      <Panel title="Registros">
        <div className="space-y-4">
          <div className="p-4 bg-blanco border rounded">
            <p className="font-plex text-petro">
              Turno 3 – Noche – Móvil 04
            </p>
            <p className="font-mono text-azul">Gasas usadas: 15</p>
          </div>
        </div>
      </Panel>
    </div>
  );
}
