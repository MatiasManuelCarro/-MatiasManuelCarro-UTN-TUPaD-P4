import { useEffect, useState } from "react";
import { Panel } from "../components/Panel";
import { BtnPrimary } from "../components/Base/BtnPrimary";

export default function AdminUsuarios() {
  const [usuarios, setUsuarios] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Modales
  const [showModal, setShowModal] = useState(false);
  const [editModal, setEditModal] = useState(false);

  // Form crear usuario
  const [nuevoUsuario, setNuevoUsuario] = useState({
    nombre: "",
    email: "",
    rol: "",
  });

  // Form editar usuario
  const [usuarioEdit, setUsuarioEdit] = useState<any>(null);

  // GET usuarios
  useEffect(() => {
    fetch("http://localhost:8000/usuarios")
      .then((r) => r.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setUsuarios(data);
        } else {
          setError("Formato inválido en backend");
        }
      })
      .catch(() => setError("No se pudo cargar usuarios"))
      .finally(() => setLoading(false));
  }, []);

  // POST crear usuario
  const crearUsuario = () => {
    fetch("http://localhost:8000/usuarios", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(nuevoUsuario),
    })
      .then((r) => r.json())
      .then((data) => {
        setUsuarios((prev) => [...prev, data]);
        setShowModal(false);
        setNuevoUsuario({ nombre: "", email: "", rol: "" });
      })
      .catch(() => alert("Error al crear usuario"));
  };

  // PUT editar usuario
  const guardarEdicion = () => {
    fetch(`http://localhost:8000/usuarios/${usuarioEdit.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(usuarioEdit),
    })
      .then((r) => r.json())
      .then((data) => {
        setUsuarios((prev) =>
          prev.map((u) => (u.id === data.id ? data : u))
        );
        setEditModal(false);
      })
      .catch(() => alert("Error al editar usuario"));
  };

  // Abrir modal editar
  const abrirEditar = (usuario: any) => {
    setUsuarioEdit(usuario);
    setEditModal(true);
  };

  if (loading) {
    return <div className="p-10 text-petro animate-pulse">Cargando usuarios...</div>;
  }

  if (error) {
    return (
      <div className="p-10">
        <div className="bg-coral text-white p-4 rounded-lg shadow-lg font-plex">
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-fondo p-10 font-plex text-petro flex justify-center">
      <div className="w-full max-w-5xl space-y-8">

        <h1 className="font-barlow text-4xl text-petro tracking-tight">
          Usuarios
        </h1>

        <Panel title="Listado de usuarios">
          <table className="w-full font-plex">
            <thead>
              <tr className="text-petro border-b bg-gray-50">
                <th className="p-3 text-left">Nombre</th>
                <th className="p-3 text-left">Email</th>
                <th className="p-3 text-left">Rol</th>
                <th className="p-3 text-left">Estado</th>
                <th className="p-3 text-left">Acciones</th>
              </tr>
            </thead>

            <tbody>
              {usuarios.map((u) => (
                <tr
                  key={u.id}
                  className="border-b hover:bg-gray-50 transition-all"
                >
                  <td className="p-3">{u.nombre}</td>
                  <td className="p-3">{u.email}</td>
                  <td className="p-3">{u.rol ?? "Sin rol"}</td>
                  <td className="p-3">
                    <span className="text-verde font-semibold">Activo</span>
                  </td>
                  <td className="p-3">
                    <button
                      className="text-azul hover:text-petro transition font-semibold"
                      onClick={() => abrirEditar(u)}
                    >
                      Editar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </Panel>

        <BtnPrimary onClick={() => setShowModal(true)}>
          Crear usuario
        </BtnPrimary>

        {/* MODAL CREAR */}
        {showModal && (
          <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-center items-center">
            <div className="bg-white w-full max-w-md p-8 rounded-2xl shadow-2xl">

              <h2 className="text-2xl font-barlow mb-6">Nuevo usuario</h2>

              <div className="space-y-4">
                <input
                  type="text"
                  placeholder="Nombre"
                  className="w-full p-3 border rounded-lg"
                  value={nuevoUsuario.nombre}
                  onChange={(e) =>
                    setNuevoUsuario({ ...nuevoUsuario, nombre: e.target.value })
                  }
                />

                <input
                  type="email"
                  placeholder="Email"
                  className="w-full p-3 border rounded-lg"
                  value={nuevoUsuario.email}
                  onChange={(e) =>
                    setNuevoUsuario({ ...nuevoUsuario, email: e.target.value })
                  }
                />

                <input
                  type="text"
                  placeholder="Rol"
                  className="w-full p-3 border rounded-lg"
                  value={nuevoUsuario.rol}
                  onChange={(e) =>
                    setNuevoUsuario({ ...nuevoUsuario, rol: e.target.value })
                  }
                />
              </div>

              <div className="flex justify-end gap-3 mt-6">
                <button
                  className="px-4 py-2 rounded-lg bg-gray-200 hover:bg-gray-300 transition"
                  onClick={() => setShowModal(false)}
                >
                  Cancelar
                </button>

                <button
                  className="px-4 py-2 rounded-lg bg-turquesa text-white hover:bg-petro transition"
                  onClick={crearUsuario}
                >
                  Crear
                </button>
              </div>

            </div>
          </div>
        )}

        {/* MODAL EDITAR */}
        {editModal && usuarioEdit && (
          <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex justify-center items-center">
            <div className="bg-white w-full max-w-md p-8 rounded-2xl shadow-2xl">

              <h2 className="text-2xl font-barlow mb-6">Editar usuario</h2>

              <div className="space-y-4">
                <input
                  type="text"
                  className="w-full p-3 border rounded-lg"
                  value={usuarioEdit.nombre}
                  onChange={(e) =>
                    setUsuarioEdit({ ...usuarioEdit, nombre: e.target.value })
                  }
                />

                <input
                  type="email"
                  className="w-full p-3 border rounded-lg"
                  value={usuarioEdit.email}
                  onChange={(e) =>
                    setUsuarioEdit({ ...usuarioEdit, email: e.target.value })
                  }
                />

                <input
                  type="text"
                  className="w-full p-3 border rounded-lg"
                  value={usuarioEdit.rol}
                  onChange={(e) =>
                    setUsuarioEdit({ ...usuarioEdit, rol: e.target.value })
                  }
                />
              </div>

              <div className="flex justify-end gap-3 mt-6">
                <button
                  className="px-4 py-2 rounded-lg bg-gray-200 hover:bg-gray-300 transition"
                  onClick={() => setEditModal(false)}
                >
                  Cancelar
                </button>

                <button
                  className="px-4 py-2 rounded-lg bg-turquesa text-white hover:bg-petro transition"
                  onClick={guardarEdicion}
                >
                  Guardar cambios
                </button>
              </div>

            </div>
          </div>
        )}

      </div>
    </div>
  );
}
