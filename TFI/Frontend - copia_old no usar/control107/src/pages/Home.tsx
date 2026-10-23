import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="min-h-screen bg-fondo p-10 font-plex text-petro">

      <h1 className="text-3xl font-barlow mb-8">
        Navegación principal
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

        {/* Login */}
        <Link
          to="/"
          className="bg-turquesa text-white p-5 rounded-lg shadow hover:bg-petro transition block"
        >
          Login
        </Link>

        {/* Enfermero */}
        <Link
          to="/operativo"
          className="bg-turquesa text-white p-5 rounded-lg shadow hover:bg-petro transition block"
        >
          Panel del Enfermero
        </Link>

        {/* Administración */}
        <Link
          to="/admin/dashboard"
          className="bg-turquesa text-white p-5 rounded-lg shadow hover:bg-petro transition block"
        >
          Dashboard Administrativo
        </Link>

        <Link
          to="/admin/usuarios"
          className="bg-turquesa text-white p-5 rounded-lg shadow hover:bg-petro transition block"
        >
          Gestión de Usuarios
        </Link>

        <Link
          to="/admin/ambulancias"
          className="bg-turquesa text-white p-5 rounded-lg shadow hover:bg-petro transition block"
        >
          Ambulancias
        </Link>

        <Link
          to="/admin/insumos"
          className="bg-turquesa text-white p-5 rounded-lg shadow hover:bg-petro transition block"
        >
          Insumos
        </Link>

        <Link
          to="/admin/turnos"
          className="bg-turquesa text-white p-5 rounded-lg shadow hover:bg-petro transition block"
        >
          Turnos
        </Link>

        <Link
          to="/admin/historial"
          className="bg-turquesa text-white p-5 rounded-lg shadow hover:bg-petro transition block"
        >
          Historial
        </Link>

      </div>
    </div>
  );
}
