// src/components/UI/Input.tsx
import type { InputHTMLAttributes } from "react";

type InputProps = InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
};

export function Input({ label, ...props }: InputProps) {
  return (
    <div className="flex flex-col gap-2">
      {label && (
        <label className="font-barlow text-petro text-[15px]">
          {label}
        </label>
      )}

      <input
        {...props}
        className="border border-fondo p-3 rounded font-plex text-petro focus:outline-none focus:ring-2 focus:ring-turquesa"
      />
    </div>
  );
}
