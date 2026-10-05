import { useCategorias } from "../hooks/useCategorias";
import CategoriaList from "../components/CategoriaList";
import CategoriaModal from "../components/CategoriaModal";

export default function CategoriasPage() {
    const {
        categorias,
        modalAbierta,
        categoriaSeleccionada,
        abrirModalCrear,
        abrirModalEditar,
        cerrarModal,
        handleCreate,
        handleUpdate,
        handleDelete,
    } = useCategorias();

    return (
        <div className="max-w-3xl mx-auto">  
            {/* Encabezado */}
            <div className="flex justify-between items-center mb-4">
                <h1 className="text-xl font-semibold">Categorías</h1>

                <button
                    className="w-40 py-3 active:scale-95 transition text-sm text-white rounded-lg bg-indigo-500 hover:bg-indigo-500/80 cursor-pointer flex items-center justify-center gap-1 "
                    onClick={abrirModalCrear}
                >
                    + Añadir Categoría
                </button>
            </div>

            <div className="w-full bg-slate-100 border border-neutral-300 rounded-xl p-6 shadow-sm">
                <CategoriaList
                    categorias={categorias}
                    onEdit={abrirModalEditar}
                    onDelete={handleDelete}
                />
            </div>

            <CategoriaModal
                abierta={modalAbierta}
                categoria={categoriaSeleccionada}
                onClose={cerrarModal}
                onSubmit={(data) =>
                    categoriaSeleccionada
                        ? handleUpdate(categoriaSeleccionada.id, data)
                        : handleCreate(data)
                }
            />
        </div>
    );
}
