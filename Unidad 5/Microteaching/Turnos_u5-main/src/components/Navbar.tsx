// Barra de navegacion. No recibe props: siempre muestra lo mismo.
function Navbar() {
  return (
    <header className="bg-teal-700 text-white">
      <nav className="mx-auto flex max-w-4xl items-center justify-between px-4 py-4">
        <span className="text-lg font-bold">Gestor de Turnos</span>
        <ul className="flex gap-4 text-sm">
          <li>Turnos</li>
          <li>Pacientes</li>
          <li>Profesionales</li>
        </ul>
      </nav>
    </header>
  )
}

export default Navbar
