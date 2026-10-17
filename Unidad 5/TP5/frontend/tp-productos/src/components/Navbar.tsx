// Barra de navegacion. No recibe props: siempre muestra lo mismo.
function Navbar() {
  return (
    <header className="bg-gradient-to-b from-gray-800 to-gray-900 text-white">
      <nav className="mx-auto flex max-w-4xl items-center justify-between px-5 py-6 xl:px-12">
        <span className="font-heading text-3xl font-bold">TPI Productos</span>

        <ul className="flex gap-6 text-sm">
          <li className="text-sm tracking-wide transition-all hover:scale-[1.01] hover:font-medium hover:text-slate-300 hover:drop-shadow-sm md:text-base">
            Productos
          </li>
          <li className="text-sm tracking-wide transition-all hover:scale-[1.01] hover:font-medium hover:text-slate-300 hover:drop-shadow-sm md:text-base">
            Categorías
          </li>
          <li className="text-sm tracking-wide transition-all hover:scale-[1.01] hover:font-medium hover:text-slate-300 hover:drop-shadow-sm md:text-base">
            Proveedores
          </li>
        </ul>
      </nav>
    </header>
  );
}

export default Navbar;
