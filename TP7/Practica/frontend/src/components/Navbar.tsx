import { Link } from "react-router-dom";

export const Navbar = () => {
    return (
        <nav className="flex items-center justify-between bg-slate-800 px-6 py-4 text-white">
            <h1 className="text-xl font-bold">
                Catálogo
            </h1>

            <div className="flex gap-4">
                <Link
                    to="/categorias"
                    className="hover:text-blue-400"
                >
                    Categorías
                </Link>

                <Link
                    to="/productos"
                    className="hover:text-blue-400"
                >
                    Productos
                </Link>
            </div>
        </nav>
    );
};