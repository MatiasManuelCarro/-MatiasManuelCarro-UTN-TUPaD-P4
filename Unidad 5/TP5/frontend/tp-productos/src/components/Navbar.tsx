// Barra de navegacion. No recibe props: siempre muestra lo mismo.
function Navbar() {
    return (
        <header className="bg-gradient-to-b from-gray-800 to-gray-900 text-white">
            <nav className="mx-auto flex max-w-4xl items-center justify-between px-5 xl:px-12 py-6">

                <span className="text-3xl font-bold font-heading">
                    TPI Productos
                </span>

                <ul className="flex gap-6 text-sm">
                    <li className="text-sm md:text-base tracking-wide transition-all hover:text-slate-300 hover:drop-shadow-sm hover:font-medium hover:scale-[1.01]">Productos</li>
                    <li className="text-sm md:text-base tracking-wide transition-all hover:text-slate-300 hover:drop-shadow-sm hover:font-medium hover:scale-[1.01]">Categorías</li>
                    <li className="text-sm md:text-base tracking-wide transition-all hover:text-slate-300 hover:drop-shadow-sm hover:font-medium hover:scale-[1.01]">Proveedores</li>
                </ul>

            </nav>
        </header>
    )
}

export default Navbar