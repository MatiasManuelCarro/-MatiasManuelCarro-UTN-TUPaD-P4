// src/components/Base/Panel.tsx
import type { ReactNode } from "react";

type PanelProps = {
  title: ReactNode;
  children: ReactNode;
};

export function Panel({ title, children }: PanelProps) {
  return (
    <div className="bg-blanco p-6 rounded border border-fondo shadow-sm">
      <h3 className="font-barlow text-xl text-petro mb-4">{title}</h3>
      {children}
    </div>
  );
}
