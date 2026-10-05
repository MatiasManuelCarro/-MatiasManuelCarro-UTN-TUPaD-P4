function Navbar() {
  return (
    <header className="h-17.5 w-full px-6 md:px-16 lg:px-24 xl:px-32 flex items-center bg-linear-to-r from-indigo-700 to-violet-500">
      <nav className="w-full flex items-center justify-between">

        <div className="flex items-center gap-3">
          <img src="/icon_white.svg" alt="logo" className="w-10 h-10" />

          <span className="text-2xl font-outfit text-white font-bold tracking-wide">
            TP Categorías
          </span>
        </div>

        <ul className="text-white md:flex hidden items-center gap-10">
          <li><a className="hover:text-white/70 transition" href="#">Home</a></li>
          <li><a className="hover:text-white/70 transition" href="#">Categorías</a></li>
        </ul>

      </nav>
    </header>
  );
}

export default Navbar;
