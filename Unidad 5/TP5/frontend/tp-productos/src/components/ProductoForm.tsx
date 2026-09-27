export default function ProductoForm() {
    return (
        <form className="border rounded-md bg-white p-4 shadow-sm">
            <h2 className="text-slate-850 text-xl tracking-wide font-bold mb-4">Nuevo Producto</h2>

            <div className="flex flex-col gap-4">
                <input
                    type="text"
                    placeholder="Nombre"
                    className="w-full p-2 rounded text-slate-700 border border-slate-700 placeholder-slate-400 transition-all focus:outline-none focus:bg-slate-600 focus:ring-2 focus:ring-cyan-700 focus:text-white"
                />

                <input
                    type="text"
                    placeholder="Descripción"
                    className="w-full p-2 rounded text-slate-700 border border-slate-700 placeholder-slate-400 transition-all focus:outline-none focus:bg-slate-600 focus:ring-2 focus:ring-cyan-700 focus:text-white"
                />

                <input
                    type="number"
                    placeholder="Precio"
                    className="w-full p-2 rounded text-slate-700 border border-slate-700 placeholder-slate-400 transition-all focus:outline-none focus:bg-slate-600 focus:ring-2 focus:ring-cyan-700 focus:text-white" />
                

                <button
                    type="button"
                    className="bg-transparent hover:bg-slate-600 text-slate-600 font-semibold hover:text-white py-2 px-4 border border-slate-700 hover:border-transparent rounded transition-all duration-200 ease-in-out"
                >
                    Guardar
                </button>
            </div>
        </form>
    );
}
