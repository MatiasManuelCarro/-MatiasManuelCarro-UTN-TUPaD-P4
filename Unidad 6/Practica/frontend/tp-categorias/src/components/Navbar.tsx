function Navbar() {
  return (
    <header className="bg-gradient-to-b from-neutral-900 to-neutral-800 text-neutral-100">
      <nav className="mx-auto flex max-w-4xl items-center justify-between px-5 xl:px-12 py-6">

        <span className="text-2xl font-bold tracking-wide">
          TP Categorías
        </span>

        <ul className="flex gap-6 text-sm">
          <li className="transition-all hover:text-neutral-300 hover:drop-shadow-sm hover:font-medium hover:scale-[1.01]">
            Categorías
          </li>
        </ul>

      </nav>
    </header>
  );
}

export default Navbar;
