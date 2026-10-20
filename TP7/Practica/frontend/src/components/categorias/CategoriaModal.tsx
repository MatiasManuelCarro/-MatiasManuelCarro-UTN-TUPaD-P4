import { useState } from "react";

import type {
  Categoria,
  CategoriaCreate,
} from "../../types/Categoria";

type CategoriaModalProps = {
  categoria: Categoria | null;
  isPending: boolean;
  errorMessage: string | null;
  onClose: () => void;
  onSubmit: (categoria: CategoriaCreate) => void;
};

export const CategoriaModal = ({
  categoria,
  isPending,
  errorMessage,
  onClose,
  onSubmit,
}: CategoriaModalProps) => {
  const [nombre, setNombre] = useState(
    categoria?.nombre ?? "",
  );

  const [descripcion, setDescripcion] = useState(
    categoria?.descripcion ?? "",
  );

  const esEdicion = categoria !== null;

  return (
    <div
      className="fixed inset-0 flex items-center justify-center bg-black/60 p-4"
      onClick={onClose}
    >
      <div
        className="w-full max-w-md rounded bg-white p-6 text-slate-900"
        onClick={(event) => event.stopPropagation()}
      >
        <h2 className="mb-4 text-xl font-bold">
          {esEdicion
            ? "Editar categoría"
            : "Nueva categoría"}
        </h2>

        <form
          className="space-y-4"
          onSubmit={(event) => {
            event.preventDefault();

            const nombreLimpio = nombre.trim();

            if (!nombreLimpio) {
              return;
            }

            onSubmit({
              nombre: nombreLimpio,
              descripcion: descripcion.trim(),
            });
          }}
        >
          <div>
            <label
              htmlFor="nombre"
              className="mb-1 block font-medium"
            >
              Nombre
            </label>

            <input
              id="nombre"
              type="text"
              value={nombre}
              onChange={(event) =>
                setNombre(event.target.value)
              }
              maxLength={100}
              required
              className="w-full rounded border border-slate-300 p-2"
            />
          </div>

          <div>
            <label
              htmlFor="descripcion"
              className="mb-1 block font-medium"
            >
              Descripción
            </label>

            <textarea
              id="descripcion"
              value={descripcion}
              onChange={(event) =>
                setDescripcion(event.target.value)
              }
              className="w-full rounded border border-slate-300 p-2"
            />
          </div>

          {errorMessage && (
            <p className="text-sm text-red-600">
              {errorMessage}
            </p>
          )}

          <div className="flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              disabled={isPending}
              className="rounded bg-slate-500 px-4 py-2 text-white disabled:opacity-50"
            >
              Cancelar
            </button>

            <button
              type="submit"
              disabled={isPending}
              className="rounded bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
            >
              {isPending
                ? "Guardando..."
                : "Guardar"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};