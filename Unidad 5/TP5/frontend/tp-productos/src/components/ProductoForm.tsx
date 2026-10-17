export default function ProductoForm() {
  return (
    <form className="rounded-md border bg-white p-4 shadow-sm">
      <h2 className="text-slate-850 mb-4 text-xl font-bold tracking-wide">
        Nuevo Producto
      </h2>

      <div className="flex flex-col gap-4">
        <input
          type="text"
          placeholder="Nombre"
          className="w-full rounded border border-slate-700 p-2 text-slate-700 placeholder-slate-400 transition-all focus:bg-slate-600 focus:text-white focus:ring-2 focus:ring-cyan-700 focus:outline-none"
        />

        <input
          type="text"
          placeholder="Descripción"
          className="w-full rounded border border-slate-700 p-2 text-slate-700 placeholder-slate-400 transition-all focus:bg-slate-600 focus:text-white focus:ring-2 focus:ring-cyan-700 focus:outline-none"
        />

        <input
          type="number"
          placeholder="Precio"
          className="w-full rounded border border-slate-700 p-2 text-slate-700 placeholder-slate-400 transition-all focus:bg-slate-600 focus:text-white focus:ring-2 focus:ring-cyan-700 focus:outline-none"
        />

        <button
          type="button"
          className="rounded border border-slate-700 bg-transparent px-4 py-2 font-semibold text-slate-600 transition-all duration-200 ease-in-out hover:border-transparent hover:bg-slate-600 hover:text-white"
        >
          Guardar
        </button>
      </div>
    </form>
  );
}
