// src/components/Base/BtnSecondary.tsx
import type { ButtonHTMLAttributes, ReactNode } from "react";

type BtnProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
};

export function BtnSecondary({ children, ...props }: BtnProps) {
  return (
    <button
      {...props}
      className="border border-turquesa text-turquesa font-plex px-4 py-2 rounded hover:bg-fondo transition"
    >
      {children}
    </button>
  );
}
