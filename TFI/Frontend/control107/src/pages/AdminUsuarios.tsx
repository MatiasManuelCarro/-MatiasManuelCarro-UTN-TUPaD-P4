import { useEffect, useState } from "react";
import { Panel } from "../components/Panel";
import { BtnPrimary } from "../components/Base/BtnPrimary";
import {
  actualizarUsuario,
  crearUsuario,
  eliminarUsuario,
  listarUsuarios,
} from "../services/usuarios";
import type {
  CrearUsuarioRequest,
  EditarUsuarioRequest,
  RolUsuario,
  Usuario,
} from "../interfaces/Usuario";

const usuarioInicial: CrearUsuarioRequest = {
  nombre: "",
  dni: "",
  email: "",
  rol: "ENFERMERO",
  clave: "",
  activo: true,
};

export default function AdminUsuarios() {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);

  const [loading, setLoading] = useState(true);
  const [guardando, setGuardando] = useState(false);
  const [error, setError] = useState("");

  const [showModal, setShowModal] = useState(false);
  const [editModal, setEditModal] = useState(false);

  const [nuevoUsuario, setNuevoUsuario] =
    useState<CrearUsuarioRequest>(usuarioInicial);

  const [usuarioEdit, setUsuarioEdit] =
    useState<Usuario | null>(null);

  useEffect(() => {
    cargarUsuarios();
  }, []);

  async function cargarUsuarios() {
    setLoading(true);
    setError("");

    try {
      const data = await listarUsuarios();
      setUsuarios(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "No se pudieron cargar los usuarios"
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleCrearUsuario() {
    setError("");

    if (!nuevoUsuario.nombre.trim()) {
      setError("El nombre es obligatorio");
      return;
    }

    if (!nuevoUsuario.dni.trim()) {
      setError("El DNI es obligatorio");
      return;
    }

    if (!nuevoUsuario.email.trim()) {
      setError("El email es obligatorio");
      return;
    }

    if (nuevoUsuario.clave.length < 6) {
      setError("La clave debe tener al menos 6 caracteres");
      return;
    }

    setGuardando(true);

    const request: CrearUsuarioRequest = {
      nombre: nuevoUsuario.nombre.trim(),
      dni: nuevoUsuario.dni.trim(),
      email: nuevoUsuario.email.trim(),
      rol: nuevoUsuario.rol,
      clave: nuevoUsuario.clave,
      activo: nuevoUsuario.activo,
    };

    try {
      const usuarioCreado = await crearUsuario(request);

      setUsuarios((prev) => [...prev, usuarioCreado]);
      setNuevoUsuario(usuarioInicial);
      setShowModal(false);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "No se pudo crear el usuario"
      );
    } finally {
      setGuardando(false);
    }
  }

  function abrirEditar(usuario: Usuario) {
    setError("");

    // Se crea una copia para no modificar directamente
    // el usuario que ya aparece en la tabla.
    setUsuarioEdit({ ...usuario });
    setEditModal(true);
  }

  async function handleGuardarEdicion() {
    if (!usuarioEdit) {
      return;
    }

    setError("");

    if (!usuarioEdit.nombre.trim()) {
      setError("El nombre es obligatorio");
      return;
    }

    if (!usuarioEdit.dni.trim()) {
      setError("El DNI es obligatorio");
      return;
    }

    if (!usuarioEdit.email.trim()) {
      setError("El email es obligatorio");
      return;
    }

    const request: EditarUsuarioRequest = {
      nombre: usuarioEdit.nombre.trim(),
      dni: usuarioEdit.dni.trim(),
      email: usuarioEdit.email.trim(),
      rol: usuarioEdit.rol,
      activo: usuarioEdit.activo,
    };

    setGuardando(true);

    try {
      const usuarioActualizado = await actualizarUsuario(
        usuarioEdit.id,
        request
      );

      setUsuarios((prev) =>
        prev.map((usuario) =>
          usuario.id === usuarioActualizado.id
            ? usuarioActualizado
            : usuario
        )
      );

      setUsuarioEdit(null);
      setEditModal(false);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "No se pudo actualizar el usuario"
      );
    } finally {
      setGuardando(false);
    }
  }

  async function handleEliminar(usuario: Usuario) {
    const confirmado = window.confirm(
      `¿Deseas eliminar al usuario ${usuario.nombre}?`
    );

    if (!confirmado) {
      return;
    }

    setError("");

    try {
      await eliminarUsuario(usuario.id);

      setUsuarios((prev) =>
        prev.filter((item) => item.id !== usuario.id)
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "No se pudo eliminar el usuario"
      );
    }
  }

  if (loading) {
    return (
      <div className="p-10 text-petro animate-pulse">
        Cargando usuarios...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-fondo p-10 font-plex text-petro flex justify-center">
      <div className="w-full max-w-6xl space-y-8">
        <h1 className="font-barlow text-4xl text-petro tracking-tight">
          Usuarios
        </h1>

        {error && (
          <div className="bg-coral text-white p-4 rounded-lg shadow-lg">
            {error}
          </div>
        )}

        <Panel title="Listado de usuarios">
          {usuarios.length === 0 ? (
            <p>No hay usuarios registrados.</p>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full font-plex">
                <thead>
                  <tr className="text-petro border-b bg-gray-50">
                    <th className="p-3 text-left">Nombre</th>
                    <th className="p-3 text-left">DNI</th>
                    <th className="p-3 text-left">Email</th>
                    <th className="p-3 text-left">Rol</th>
                    <th className="p-3 text-left">Estado</th>
                    <th className="p-3 text-left">Acciones</th>
                  </tr>
                </thead>

                <tbody>
                  {usuarios.map((usuario) => (
                    <tr
                      key={usuario.id}
                      className="border-b hover:bg-gray-50 transition-all"
                    >
                      <td className="p-3">
                        {usuario.nombre}
                      </td>

                      <td className="p-3">
                        {usuario.dni}
                      </td>

                      <td className="p-3">
                        {usuario.email}
                      </td>

                      <td className="p-3">
                        {usuario.rol}
                      </td>

                      <td className="p-3">
                        <span
                          className={
                            usuario.activo
                              ? "text-verde font-semibold"
                              : "text-coral font-semibold"
                          }
                        >
                          {usuario.activo
                            ? "Activo"
                            : "Inactivo"}
                        </span>
                      </td>

                      <td className="p-3">
                        <div className="flex gap-4">
                          <button
                            type="button"
                            className="text-azul hover:text-petro transition font-semibold"
                            onClick={() =>
                              abrirEditar(usuario)
                            }
                          >
                            Editar
                          </button>

                          <button
                            type="button"
                            className="text-coral hover:text-red-800 transition font-semibold"
                            onClick={() =>
                              handleEliminar(usuario)
                            }
                          >
                            Eliminar
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </Panel>

        <BtnPrimary onClick={() => setShowModal(true)}>
          Crear usuario
        </BtnPrimary>

        {showModal && (
          <div
            className="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-center items-center p-4"
            onClick={() => setShowModal(false)}
          >
            <div
              className="bg-white w-full max-w-md p-8 rounded-2xl shadow-2xl"
              onClick={(event) => event.stopPropagation()}
            >
              <h2 className="text-2xl font-barlow mb-6">
                Nuevo usuario
              </h2>

              <div className="space-y-4">
                <Campo
                  label="Nombre"
                  type="text"
                  value={nuevoUsuario.nombre}
                  onChange={(value) =>
                    setNuevoUsuario((prev) => ({
                      ...prev,
                      nombre: value,
                    }))
                  }
                />

                <Campo
                  label="DNI"
                  type="text"
                  value={nuevoUsuario.dni}
                  onChange={(value) =>
                    setNuevoUsuario((prev) => ({
                      ...prev,
                      dni: value,
                    }))
                  }
                />

                <Campo
                  label="Email"
                  type="email"
                  value={nuevoUsuario.email}
                  onChange={(value) =>
                    setNuevoUsuario((prev) => ({
                      ...prev,
                      email: value,
                    }))
                  }
                />

                <Campo
                  label="Clave"
                  type="password"
                  value={nuevoUsuario.clave}
                  onChange={(value) =>
                    setNuevoUsuario((prev) => ({
                      ...prev,
                      clave: value,
                    }))
                  }
                />

                <SelectorRol
                  value={nuevoUsuario.rol}
                  onChange={(rol) =>
                    setNuevoUsuario((prev) => ({
                      ...prev,
                      rol,
                    }))
                  }
                />

                <label className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={nuevoUsuario.activo}
                    onChange={(event) =>
                      setNuevoUsuario((prev) => ({
                        ...prev,
                        activo: event.target.checked,
                      }))
                    }
                  />

                  <span>Usuario activo</span>
                </label>
              </div>

              <div className="flex justify-end gap-3 mt-6">
                <button
                  type="button"
                  className="px-4 py-2 rounded-lg bg-gray-200 hover:bg-gray-300 transition"
                  onClick={() => {
                    setShowModal(false);
                    setNuevoUsuario(usuarioInicial);
                    setError("");
                  }}
                  disabled={guardando}
                >
                  Cancelar
                </button>

                <button
                  type="button"
                  className="px-4 py-2 rounded-lg bg-turquesa text-white hover:bg-petro transition disabled:opacity-50"
                  onClick={handleCrearUsuario}
                  disabled={guardando}
                >
                  {guardando ? "Creando..." : "Crear"}
                </button>
              </div>
            </div>
          </div>
        )}

        {editModal && usuarioEdit && (
          <div
            className="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-center items-center p-4"
            onClick={() => setEditModal(false)}
          >
            <div
              className="bg-white w-full max-w-md p-8 rounded-2xl shadow-2xl"
              onClick={(event) => event.stopPropagation()}
            >
              <h2 className="text-2xl font-barlow mb-6">
                Editar usuario
              </h2>

              <div className="space-y-4">
                <Campo
                  label="Nombre"
                  type="text"
                  value={usuarioEdit.nombre}
                  onChange={(value) =>
                    setUsuarioEdit((prev) =>
                      prev
                        ? { ...prev, nombre: value }
                        : null
                    )
                  }
                />

                <Campo
                  label="DNI"
                  type="text"
                  value={usuarioEdit.dni}
                  onChange={(value) =>
                    setUsuarioEdit((prev) =>
                      prev
                        ? { ...prev, dni: value }
                        : null
                    )
                  }
                />

                <Campo
                  label="Email"
                  type="email"
                  value={usuarioEdit.email}
                  onChange={(value) =>
                    setUsuarioEdit((prev) =>
                      prev
                        ? { ...prev, email: value }
                        : null
                    )
                  }
                />

                <SelectorRol
                  value={usuarioEdit.rol}
                  onChange={(rol) =>
                    setUsuarioEdit((prev) =>
                      prev ? { ...prev, rol } : null
                    )
                  }
                />

                <label className="flex items-center gap-3">
                  <input
                    type="checkbox"
                    checked={usuarioEdit.activo}
                    onChange={(event) =>
                      setUsuarioEdit((prev) =>
                        prev
                          ? {
                              ...prev,
                              activo: event.target.checked,
                            }
                          : null
                      )
                    }
                  />

                  <span>Usuario activo</span>
                </label>
              </div>

              <div className="flex justify-end gap-3 mt-6">
                <button
                  type="button"
                  className="px-4 py-2 rounded-lg bg-gray-200 hover:bg-gray-300 transition"
                  onClick={() => {
                    setEditModal(false);
                    setUsuarioEdit(null);
                    setError("");
                  }}
                  disabled={guardando}
                >
                  Cancelar
                </button>

                <button
                  type="button"
                  className="px-4 py-2 rounded-lg bg-turquesa text-white hover:bg-petro transition disabled:opacity-50"
                  onClick={handleGuardarEdicion}
                  disabled={guardando}
                >
                  {guardando
                    ? "Guardando..."
                    : "Guardar cambios"}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

interface CampoProps {
  label: string;
  type: "text" | "email" | "password";
  value: string;
  onChange: (value: string) => void;
}

function Campo({
  label,
  type,
  value,
  onChange,
}: CampoProps) {
  return (
    <label className="flex flex-col gap-2">
      <span className="font-barlow text-petro">
        {label}
      </span>

      <input
        type={type}
        className="w-full p-3 border rounded-lg"
        value={value}
        onChange={(event) =>
          onChange(event.target.value)
        }
      />
    </label>
  );
}

interface SelectorRolProps {
  value: RolUsuario;
  onChange: (rol: RolUsuario) => void;
}

function SelectorRol({
  value,
  onChange,
}: SelectorRolProps) {
  return (
    <label className="flex flex-col gap-2">
      <span className="font-barlow text-petro">
        Rol
      </span>

      <select
        className="w-full p-3 border rounded-lg"
        value={value}
        onChange={(event) =>
          onChange(event.target.value as RolUsuario)
        }
      >
        <option value="ENFERMERO">
          Enfermero
        </option>

        <option value="ADMINISTRADOR">
          Administrador
        </option>
      </select>
    </label>
  );
}