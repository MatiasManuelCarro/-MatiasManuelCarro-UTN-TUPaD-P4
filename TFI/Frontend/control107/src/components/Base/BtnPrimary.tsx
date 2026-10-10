// src/components/Base/BtnPrimary.tsx
import type { ButtonHTMLAttributes, ReactNode } from "react";


type BtnProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
};

export function BtnPrimary({ children, ...props }: BtnProps) {
  return (
    <button
      {...props}
      className="bg-turquesa text-white font-plex px-4 py-2 rounded hover:bg-petro transition"
    >
      {children}
    </button>
  );
}
