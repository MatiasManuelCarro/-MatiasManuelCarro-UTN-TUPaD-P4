import { useEffect, useState } from "react";

import { actualizarProducto, getProductos, getUnidades } from "./api";
import type { Producto } from "./types/producto";
import type { UnidadMedida } from "./types/unidadMedida";
import { Navbar } from "./components/Navbar"
import { Footer } from "./components/Footer"
import { ProductoList } from "./components/ProductoList";

function App() {
    const [productos, setProductos] = useState<Producto[]>([]);
    const [unidades, setUnidades] = useState<UnidadMedida[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        setLoading(true);
        setError(null);

        Promise.all([getProductos(), getUnidades()])
            .then(([productosData, unidadesData]) => {
                setProductos(productosData);
                setUnidades(unidadesData);
            })
            .catch(() => {
                setError("No se pudieron cargar los datos de productos");
            })
            .finally(() => {
                setLoading(false);
            });
    }, []);

    const handleDisponibilidad = (producto: Producto) => {
        const productoModificado = {
            ...producto,
            disponible: !producto.disponible
        }

        actualizarProducto(productoModificado).then((productoActualizado) => {
            const productosActualizados = productos.map((productoActual) => {
                if (productoActual.id === productoActualizado.id) {
                    return productoActualizado
                }

                return productoActual
            })

            setProductos(productosActualizados)
        })
    }

    if (loading) {
        return (
            <main className="min-h-screen bg-gray-50 p-8 text-gray-900">
                <p className="text-base text-gray-600">
                    Cargando productos...
                </p>
            </main>
        )
    }

    if (error) {
        return (
            <main className="min-h-screen bg-gray-50 p-8 text-gray-900">
                <p className="text-base text-red-600">
                    {error}
                </p>
            </main>
        )
    }

    if (productos.length === 0) {
        return (
            <main className="min-h-screen bg-gray-50 p-8 text-gray-900">
                <p className="text-base text-gray-600">
                    No hay productos para mostrar.
                </p>
            </main>
        )
    }

    return (
        <div className="min-h-screen bg-gray-50 text-gray-900">
            <Navbar />
            <main className="mx-auto flex max-w-7xl flex-col gap-8 px-4 py-8">
                <section className="flex flex-col gap-4">
                    <h2 className="text-2xl font-semibold">Productos</h2>

                    <ProductoList
                        productos={productos}
                        onDisponibilidad={handleDisponibilidad}
                    />
                </section>

                <section className="flex flex-col gap-4">
                    <h2 className="text-2xl font-semibold">Unidades de medida</h2>

                    <pre className="overflow-auto rounded-lg bg-white p-4 text-sm">
                        {JSON.stringify(unidades, null, 2)}
                    </pre>
                </section>
            </main>
            <Footer />
        </div>
    );
}

export default App;
