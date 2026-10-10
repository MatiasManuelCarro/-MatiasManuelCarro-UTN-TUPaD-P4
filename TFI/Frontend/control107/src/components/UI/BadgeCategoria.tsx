// src/components/UI/BadgeCategoria.tsx
import type { ReactNode } from "react";

type BadgeProps = {
  categoriaId: number;
  children: ReactNode;
};

const categoriaClasses: Record<number, string> = {
  1: "bg-coral text-white",     // Farmacológicos
  2: "bg-ambar text-white",     // Gotas / comprimidos
  3: "bg-turquesa text-white",  // Descartables / curación
  4: "bg-azul text-white",      // Vía aérea
  5: "bg-verde text-white",     // Equipamiento
  6: "bg-coral text-white",     // Oxígeno (naranja de atención)
};

export function BadgeCategoria({ categoriaId, children }: BadgeProps) {
  return (
    <span
      className={`px-3 py-1 rounded font-plex text-sm ${categoriaClasses[categoriaId]}`}
    >
      {children}
    </span>
  );
}
