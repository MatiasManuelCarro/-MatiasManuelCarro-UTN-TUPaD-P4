import { useState } from "react";

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {
  createCategoria,
  deleteCategoria,
  getCategorias,
  updateCategoria,
} from "../services/Categoria";

import { CategoriaList } from "../components/categorias/CategoriaList";
import { CategoriaModal } from "../components/categorias/CategoriaModal";

import type {
  Categoria,
  CategoriaCreate,
} from "../types/Categoria";

type UpdateCategoriaVariables = {
  id: number;
  categoria: CategoriaCreate;
};

export const CategoriasPage = () => {
  const queryClient = useQueryClient();

  const [modalOpen, setModalOpen] =
    useState(false);

  const [
    categoriaSeleccionada,
    setCategoriaSeleccionada,
  ] = useState<Categoria | null>(null);

  const categoriasQuery = useQuery({
    queryKey: ["categorias"],
    queryFn: getCategorias,
  });

  const closeModal = () => {
    setModalOpen(false);
    setCategoriaSeleccionada(null);
  };

  const createMutation = useMutation({
    mutationFn: createCategoria,

    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey: ["categorias"],
      });

      closeModal();
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({
      id,
      categoria,
    }: UpdateCategoriaVariables) =>
      updateCategoria(id, categoria),

    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey: ["categorias"],
      });

      closeModal();
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deleteCategoria,

    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey: ["categorias"],
      });
    },
  });

  const handleNewCategoria = () => {
    createMutation.reset();
    updateMutation.reset();

    setCategoriaSeleccionada(null);
    setModalOpen(true);
  };

  const handleEditCategoria = (
    categoria: Categoria,
  ) => {
    createMutation.reset();
    updateMutation.reset();

    setCategoriaSeleccionada(categoria);
    setModalOpen(true);
  };

  const handleDeleteCategoria = (id: number) => {
    const confirmar = window.confirm(
      "¿Deseas eliminar esta categoría?",
    );

    if (!confirmar) {
      return;
    }

    deleteMutation.mutate(id);
  };

  const handleSubmit = (
    categoria: CategoriaCreate,
  ) => {
    if (categoriaSeleccionada) {
      updateMutation.mutate({
        id: categoriaSeleccionada.id,
        categoria,
      });

      return;
    }

    createMutation.mutate(categoria);
  };

  if (categoriasQuery.isPending) {
    return <p className="p-4">Cargando...</p>;
  }

  if (categoriasQuery.isError) {
    return (
      <p className="p-4 text-red-500">
        {categoriasQuery.error.message}
      </p>
    );
  }

  const activeMutation = categoriaSeleccionada
    ? updateMutation
    : createMutation;

  return (
    <main className="p-4">
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-xl font-bold">
          Categorías
        </h1>

        <button
          type="button"
          onClick={handleNewCategoria}
          className="rounded bg-blue-600 px-4 py-2 text-white transition-all duration-200 hover:bg-blue-400 cursor-pointer"
        >
          Nueva categoría
        </button>
      </div>

      {deleteMutation.isError && (
        <p className="mb-4 text-red-500">
          {deleteMutation.error.message}
        </p>
      )}

      <CategoriaList
        categorias={categoriasQuery.data.items}
        onEdit={handleEditCategoria}
        onDelete={handleDeleteCategoria}
      />

      {modalOpen && (
        <CategoriaModal
          key={categoriaSeleccionada?.id ?? "nueva"}
          categoria={categoriaSeleccionada}
          isPending={activeMutation.isPending}
          errorMessage={
            activeMutation.isError
              ? activeMutation.error.message
              : null
          }
          onClose={closeModal}
          onSubmit={handleSubmit}
        />
      )}
    </main>
  );
};

export default CategoriasPage;