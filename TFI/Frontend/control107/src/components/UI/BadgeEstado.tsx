// src/components/UI/BadgeEstado.tsx
import type { ReactNode } from "react";

type Estado = "COMPLETO" | "REVISAR" | "FALTANTE" | "INFO";

type BadgeProps = {
  estado: Estado;
  children: ReactNode;
};

const estadoClasses: Record<Estado, string> = {
  COMPLETO: "bg-verde text-white",
  REVISAR: "bg-ambar text-white",
  FALTANTE: "bg-coral text-white",
  INFO: "bg-azul text-white",
};

export function BadgeEstado({ estado, children }: BadgeProps) {
  return (
    <span
      className={`px-3 py-1 rounded font-plex text-sm ${estadoClasses[estado]}`}
    >
      {children}
    </span>
  );
}
