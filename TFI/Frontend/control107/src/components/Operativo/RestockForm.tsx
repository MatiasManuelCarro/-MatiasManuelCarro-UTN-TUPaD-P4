// src/components/Operativo/RestockForm.tsx
export default function RestockForm() {
  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-2">
        <label className="font-barlow text-petro">Reposición de gasas</label>
        <input className="border p-2 rounded font-plex" type="number" />
      </div>
    </div>
  );
}
