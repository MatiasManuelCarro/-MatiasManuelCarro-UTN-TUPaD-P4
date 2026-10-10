// src/components/Operativo/EgresoForm.tsx
export default function EgresoForm() {
  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-2">
        <label className="font-barlow text-petro">Gasas restantes</label>
        <input className="border p-2 rounded font-plex" type="number" />
      </div>
    </div>
  );
}
