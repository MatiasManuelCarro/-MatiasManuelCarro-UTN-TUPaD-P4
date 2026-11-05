import { useEffect, useState } from "react";

import { getProductos, getUnidades } from "./api";
import type { Producto } from "./types/producto";
import type { UnidadMedida } from "./types/unidadMedida";

function App() {
    const [productos, setProductos] = useState<Producto[]>([]);
    const [unidades, setUnidades] = useState<UnidadMedida[]>([]);

    useEffect(() => {
        getProductos().then((data) => {
            setProductos(data);
        });

        getUnidades().then((data) => {
            setUnidades(data);
        });
    }, []);

    return (
        <div className="min-h-screen bg-gray-50 text-gray-900">
            <main className="mx-auto flex max-w-7xl flex-col gap-8 px-4 py-8">
                <header>
                    <h1 className="text-3xl font-bold tracking-tight">Food Store</h1>

                    <p className="mt-2 text-sm text-gray-600">
                        Administracion del catálogo de productos
                    </p>
                </header>

                <section className="flex flex-col gap-4">
                    <h2 className="text-2xl font-semibold">Productos</h2>

                    <pre className="overflow-auto rounded-lg bg-white p-4 text-sm">
                        {JSON.stringify(productos, null, 2)}
                    </pre>
                </section>

                <section className="flex flex-col gap-4">
                    <h2 className="text-2xl font-semibold">
                        Unidades de medida
                    </h2>

                    <pre className="overflow-auto rounded-lg bg-white p-4 text-sm">
                        {JSON.stringify(unidades, null, 2)}
                    </pre>
                </section>

            </main>
        </div>
    );
}

export default App;
