import type { UnidadMedida } from "../types/unidadMedida";
import { useState } from "react";
import type { SubmitEvent } from "react";
import { actualizarProducto, crearProducto } from "../api"
import type { Producto } from "../types/producto"


interface ProductoModalProps {
    unidades: UnidadMedida[];
    producto: Producto | null
    onCerrar: () => void;
    onProductoCreado: (producto: Producto) => void
    onProductoActualizado: (producto: Producto) => void
}

const fieldClassName = "flex items-center gap-4 px-2 py-2";

const labelClassName = "w-20 text-sm font-semibold text-gray-800";

const inputClassName =
    "rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 outline-none placeholder:text-gray-400 focus:border-slate-700 focus:ring-2 focus:ring-blue-100";

export function ProductoModal({ unidades, producto, onCerrar, onProductoCreado, onProductoActualizado }: ProductoModalProps) {
    const [form, setForm] = useState({
        nombre: producto?.nombre ?? "",
        descripcion: producto?.descripcion ?? "",
        precio_base: producto?.precio_base ?? "",
        unidad_venta_id: producto ? String(producto.unidad_venta_id) : "",
        stock_cantidad: producto?.stock_cantidad ?? "",
        disponible: producto?.disponible ?? true,
    });

    const [mensaje, setMensaje] = useState("");

    const handleSubmit = (event: SubmitEvent<HTMLFormElement>) => {
        event.preventDefault();

        const datosFormulario = {
            ...form,
            unidad_venta_id: Number(form.unidad_venta_id),
        };

        if (producto) {
            const productoModificado = {
                ...producto,
                ...datosFormulario
            }

            actualizarProducto(productoModificado).then((ProductoActualizado) => {
                onProductoActualizado(ProductoActualizado)
                onCerrar()
            })

            return

        }

        crearProducto({
            ...datosFormulario,
            precio_base: Number(datosFormulario.precio_base),
            stock_cantidad: Number(datosFormulario.stock_cantidad),
        }).then((productoCreado) => {
            onProductoCreado(productoCreado)

            setMensaje("Producto creado correctamente");

            setForm({
                nombre: "",
                descripcion: "",
                precio_base: "",
                unidad_venta_id: "",
                stock_cantidad: "",
                disponible: true,
            });

            setTimeout(() => {
                setMensaje("");
            }, 5000);
        });
    };

    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black/40 p-4">
            <div className="w-full max-w-lg rounded-lg bg-white p-6">
                <div className="flex items-center justify-between gap-4">
                    <h2 className="text-xl mb-4 font-semibold text-gray-900">
                        {producto ? "Editar Producto" : "Nuevo Producto"}
                    </h2>

                    <button
                        type="button"
                        onClick={onCerrar}
                        className="text-sm text-gray-600 hover:text-gray-900 hover:cursor-pointer"
                    >
                        Cerrar
                    </button>
                </div>

                {/* Formulario crear */}
                <form onSubmit={handleSubmit}>
                    {/* Nombre */}
                    <div className={fieldClassName}>
                        <label htmlFor="nombre" className={labelClassName}>
                            Nombre:
                        </label>

                        <input
                            id="nombre"
                            name="nombre"
                            type="text"
                            value={form.nombre}
                            onChange={(event) => {
                                setForm({
                                    ...form,
                                    nombre: event.target.value,
                                });
                            }}
                            className={inputClassName}
                        />
                    </div>

                    {/* Descripcion */}
                    <div className={fieldClassName}>
                        <label htmlFor="descripcion" className={labelClassName}>
                            Descripción:
                        </label>

                        <input
                            id="descripcion"
                            name="descripcion"
                            type="text"
                            value={form.descripcion}
                            onChange={(event) => {
                                setForm({
                                    ...form,
                                    descripcion: event.target.value,
                                });
                            }}
                            className={inputClassName}
                        />
                    </div>

                    {/* Precio  */}

                    <div className={fieldClassName}>
                        <label htmlFor="precio_base" className={labelClassName}>
                            Precio:
                        </label>

                        <input
                            id="precio_base"
                            name="precio_base"
                            type="number"
                            min="0"
                            step="0.01"
                            value={form.precio_base}
                            onChange={(event) => {
                                setForm({
                                    ...form,
                                    precio_base: event.target.value,
                                });
                            }}
                            className={inputClassName}
                        />
                    </div>

                    {/* stock */}

                    <div className={fieldClassName}>
                        <label htmlFor="stock_cantidad" className={labelClassName}>
                            Stock:
                        </label>

                        <input
                            id="stock_cantidad"
                            name="stock_cantidad"
                            type="number"
                            min="0"
                            step="any"
                            value={form.stock_cantidad}
                            onChange={(event) => {
                                setForm({
                                    ...form,
                                    stock_cantidad: event.target.value,
                                });
                            }}
                            className={inputClassName}
                        />
                    </div>

                    {/* Unidad de venta */}

                    <div className={fieldClassName}>
                        <label htmlFor="unidad_venta_id" className={labelClassName}>
                            Unidad:
                        </label>

                        <select
                            id="unidad_venta_id"
                            name="unidad_venta_id"
                            value={form.unidad_venta_id}
                            onChange={(event) => {
                                setForm({
                                    ...form,
                                    unidad_venta_id: event.target.value,
                                });
                            }}
                            className={inputClassName}
                        >
                            <option value="">Seleccionar unidad</option>

                            {unidades.map((unidad) => (
                                <option key={unidad.id} value={unidad.id}>
                                    {unidad.nombre} ({unidad.simbolo})
                                </option>
                            ))}
                        </select>
                    </div>

                    {/* Boton crear */}
                    <div className="mt-4 flex justify-end">
                        <button
                            type="submit"
                            className="rounded-lg bg-slate-800 px-4 py-2 text-sm font-semibold text-white hover:cursor-pointer hover:bg-slate-700"
                        >
                            {producto ? "Guardar cambios" : "Crear producto"}
                        </button>
                    </div>

                    {mensaje && (
                        <div className="mt-4 flex min-h-16 items-center justify-center rounded-lg border border-green-300 bg-green-50 px-4">
                            <p className="m-0 text-center text-sm font-semibold leading-none text-green-700">
                                {mensaje}
                            </p>
                        </div>
                    )}
                </form>
            </div>
        </div>
    );
}
