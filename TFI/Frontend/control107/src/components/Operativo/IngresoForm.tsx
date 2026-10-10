// src/components/Operativo/IngresoForm.tsx
export default function IngresoForm() {
  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-2">
        <label className="font-barlow text-petro">Gasas</label>
        <input className="border p-2 rounded font-plex" type="number" />
      </div>

      <div className="flex flex-col gap-2">
        <label className="font-barlow text-petro">Oxígeno (psi)</label>
        <input className="border p-2 rounded font-mono" type="number" />
      </div>
    </div>
  );
}
