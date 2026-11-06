import type { UnidadMedida } from "../types/unidadMedida";
import { useState } from "react";

interface ProductoModalProps {
    unidades: UnidadMedida[];
    onCerrar: () => void;
}

const fieldClassName = "flex items-center gap-4 px-2 py-2"

const labelClassName = "w-20 text-sm font-semibold text-gray-800"

const inputClassName =
    "rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 outline-none placeholder:text-gray-400 focus:border-slate-700 focus:ring-2 focus:ring-blue-100"

export function ProductoModal({ unidades, onCerrar }: ProductoModalProps) {
    const [form, setForm] = useState({
        nombre: "",
        descripcion: "",
        precio_base: "",
        unidad_venta_id: "",
        stock_cantidad: "",
        disponible: true,
    });
    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black/40 p-4">
            <div className="w-full max-w-lg rounded-lg bg-white p-6">
                <div className="flex items-center justify-between gap-4">
                    <h2 className="text-xl font-semibold text-gray-900">
                        Nuevo Producto
                    </h2>

                    <button
                        type="button"
                        onClick={onCerrar}
                        className="text-sm text-gray-600 hover:text-gray-900"
                    >
                        Cerrar
                    </button>
                </div>

                {/* Nombre */}
                <div className={fieldClassName}>
                    {/* <p className="text-sm text-gray-600">
                        Unidades disponibles: {unidades.length}
                    </p> */}


                    <label
                        htmlFor="nombre"
                        className={labelClassName}
                    >
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
                    <label
                        htmlFor="descripcion"
                        className={labelClassName}
                    >
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
                            })
                        }}
                        className={inputClassName}
                    />
                </div>

                {/* Precio  */}

                <div className={fieldClassName}>
                    <label
                        htmlFor="precio_base"
                        className={labelClassName}
                    >
                        Precio:
                    </label>

                    <input
                        id="precio_base"
                        name="precio_base"
                        type="number"
                        min="0"
                        step="1"
                        value={form.precio_base}
                        onChange={(event) => {
                            setForm({
                                ...form,
                                precio_base: event.target.value,
                            })
                        }}
                        className={inputClassName}
                    />
                </div>

                {/* stock */}

                <div className={fieldClassName}>
                    <label
                        htmlFor="stock_cantidad"
                        className={labelClassName}
                    >
                        Stock:
                    </label>

                    <input
                        id="stock_cantidad"
                        name="stock_cantidad"
                        type="number"
                        min="0"
                        step="1"
                        value={form.stock_cantidad}
                        onChange={(event) => {
                            setForm({
                                ...form,
                                stock_cantidad: event.target.value,
                            })
                        }}
                        className={inputClassName}
                    />
                </div>


            </div>
        </div>
    );
}
