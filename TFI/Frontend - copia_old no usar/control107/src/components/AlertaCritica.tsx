// src/components/Base/AlertaCritica.tsx
import type { ReactNode } from "react";

type AlertaProps = {
  titulo: ReactNode;
  descripcion: ReactNode;
};

export function AlertaCritica({ titulo, descripcion }: AlertaProps) {
  return (
    <div className="bg-coral text-white p-4 rounded font-plex">
      <h4 className="font-barlow text-lg">{titulo}</h4>
      <p className="text-sm">{descripcion}</p>
    </div>
  );
}
