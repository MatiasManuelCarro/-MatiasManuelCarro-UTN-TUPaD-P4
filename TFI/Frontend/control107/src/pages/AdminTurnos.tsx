import { useEffect, useState } from "react";
import { Panel } from "../components/Panel";
import { BtnPrimary } from "../components/Base/BtnPrimary";
import {
  crearTurno,
  listarTurnos,
} from "../services/turnos";
import { listarAmbulancias } from "../services/ambulancias";
import { listarEnfermerosActivos } from "../services/enfermeros";
import type {
  HorarioTurno,
  Turno,
} from "../interfaces/Turno";

interface Ambulancia {
  id: number;
  patente: string;
  disponible?: boolean;
}

interface Usuario {
  id: number;
  nombre: string;
  email: string;
  rol: "ADMINISTRADOR" | "ENFERMERO";
  activo: boolean;
}

export default function AdminTurnos() {
  const [turnos, setTurnos] = useState<Turno[]>([]);
  const [ambulancias, setAmbulancias] = useState<Ambulancia[]>([]);
  const [enfermeros, setEnfermeros] = useState<Usuario[]>([]);

  const [mostrarForm, setMostrarForm] = useState(false);
  const [cargando, setCargando] = useState(true);
  const [guardando, setGuardando] = useState(false);
  const [error, setError] = useState("");

  const [fecha, setFecha] = useState("");
  const [horario, setHorario] =
    useState<HorarioTurno>("MANIANA");

  const [ambulanciaId, setAmbulanciaId] =
    useState<number | null>(null);

  const [enfermeroId, setEnfermeroId] =
    useState<number | null>(null);

  const [chofer, setChofer] = useState("");
  const [medico, setMedico] = useState("");

  // Temporal mientras no haya login real.
  // Debe coincidir con un usuario ADMINISTRADOR existente en H2.
  // ! TODO: CHEQUAR ESTO
  const adminId = 1;

  useEffect(() => {
    async function cargarDatos() {
      setCargando(true);
      setError("");

      try {
        const [
          turnosData,
          ambulanciasData,
          enfermerosData,
        ] = await Promise.all([
          listarTurnos(),
          listarAmbulancias(),
          listarEnfermerosActivos(),
        ]);

        setTurnos(turnosData);
        setAmbulancias(ambulanciasData);
        setEnfermeros(enfermerosData);

        if (ambulanciasData.length > 0) {
          setAmbulanciaId(ambulanciasData[0].id);
        }

        if (enfermerosData.length > 0) {
          setEnfermeroId(enfermerosData[0].id);
        }
      } catch (err) {
        const mensaje =
          err instanceof Error
            ? err.message
            : "No se pudieron cargar los datos";

        setError(mensaje);
      } finally {
        setCargando(false);
      }
    }

    cargarDatos();
  }, []);

  const handleCrear = async () => {
    setError("");

    if (!fecha) {
      setError("Debes seleccionar una fecha");
      return;
    }

    if (!chofer.trim()) {
      setError("Debes ingresar el nombre del conductor");
      return;
    }

    if (!medico.trim()) {
      setError("Debes ingresar el nombre del médico");
      return;
    }

    if (ambulanciaId === null) {
      setError("No hay una ambulancia seleccionada");
      return;
    }

    if (enfermeroId === null) {
      setError("No hay un enfermero seleccionado");
      return;
    }

    setGuardando(true);

    const turnoRequest = {
      fecha,
      horario,
      adminId,
      enfermeroId,
      ambulanciaId,
      nombreChofer: chofer.trim(),
      nombreMedico: medico.trim(),
    };

    console.log("TURNO ENVIADO:", turnoRequest);

    try {
      const turnoCreado = await crearTurno(turnoRequest);

      console.log("TURNO CREADO:", turnoCreado);

      const turnosActualizados = await listarTurnos();

      setTurnos(turnosActualizados);
      setMostrarForm(false);

      setFecha("");
      setHorario("MANIANA");
      setChofer("");
      setMedico("");
    } catch (err) {
      const mensaje =
        err instanceof Error
          ? err.message
          : "No se pudo crear el turno";

      console.error("ERROR CREANDO TURNO:", err);
      setError(mensaje);
    } finally {
      setGuardando(false);
    }
  };

  if (cargando) {
    return (
      <div className="min-h-screen bg-fondo p-6">
        <p className="font-plex text-petro">
          Cargando turnos...
        </p>
      </div>
    );
  }

  return (
    <div className="min-h-screen space-y-6 bg-fondo p-6">
      <h1 className="font-barlow text-3xl text-petro">
        Turnos
      </h1>

      {error && (
        <div className="rounded bg-coral p-4 font-plex text-white">
          {error}
        </div>
      )}

      <Panel title="Programación">
        <div className="space-y-4">
          {turnos.length === 0 && (
            <p className="font-plex text-petro">
              No hay turnos registrados.
            </p>
          )}

          {turnos.map((turno) => (
            <div
              key={turno.id}
              className="flex justify-between rounded border bg-blanco p-4"
            >
              <div>
                <p className="font-plex text-petro">
                  {turno.fecha} - {turno.horario}
                </p>

                <p className="text-sm text-petro/70">
                  Ambulancia:{" "}
                  {turno.ambulancia?.patente ?? "Sin asignar"}
                </p>
              </div>

              <span className="font-mono text-azul">
                {turno.estado}
              </span>
            </div>
          ))}
        </div>
      </Panel>

      {!mostrarForm && (
        <BtnPrimary onClick={() => setMostrarForm(true)}>
          Crear turno
        </BtnPrimary>
      )}

      {mostrarForm && (
        <Panel title="Nuevo turno">
          <div className="space-y-4">
            <div className="flex flex-col gap-2">
              <label className="font-barlow text-petro">
                Fecha
              </label>

              <input
                type="date"
                className="rounded border p-2"
                value={fecha}
                onChange={(e) => setFecha(e.target.value)}
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="font-barlow text-petro">
                Horario
              </label>

              <select
                className="rounded border p-2"
                value={horario}
                onChange={(e) =>
                  setHorario(e.target.value as HorarioTurno)
                }
              >
                <option value="MANIANA">Mañana</option>
                <option value="TARDE">Tarde</option>
                <option value="NOCHE">Noche</option>
              </select>
            </div>

            <div className="flex flex-col gap-2">
              <label className="font-barlow text-petro">
                Ambulancia
              </label>

              <select
                className="rounded border p-2"
                value={ambulanciaId ?? ""}
                onChange={(e) =>
                  setAmbulanciaId(Number(e.target.value))
                }
                disabled={ambulancias.length === 0}
              >
                {ambulancias.length === 0 && (
                  <option value="">
                    No hay ambulancias disponibles
                  </option>
                )}

                {ambulancias.map((ambulancia) => (
                  <option
                    key={ambulancia.id}
                    value={ambulancia.id}
                  >
                    {ambulancia.patente}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex flex-col gap-2">
              <label className="font-barlow text-petro">
                Conductor
              </label>

              <input
                type="text"
                className="rounded border p-2"
                value={chofer}
                onChange={(e) => setChofer(e.target.value)}
                placeholder="Nombre del conductor"
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="font-barlow text-petro">
                Médico
              </label>

              <input
                type="text"
                className="rounded border p-2"
                value={medico}
                onChange={(e) => setMedico(e.target.value)}
                placeholder="Nombre del médico"
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="font-barlow text-petro">
                Enfermero
              </label>

              <select
                className="rounded border p-2"
                value={enfermeroId ?? ""}
                onChange={(e) =>
                  setEnfermeroId(Number(e.target.value))
                }
                disabled={enfermeros.length === 0}
              >
                {enfermeros.length === 0 && (
                  <option value="">
                    No hay enfermeros activos
                  </option>
                )}

                {enfermeros.map((enfermero) => (
                  <option
                    key={enfermero.id}
                    value={enfermero.id}
                  >
                    {enfermero.nombre}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex gap-3">
              <BtnPrimary
                onClick={handleCrear}
                disabled={
                  guardando ||
                  ambulanciaId === null ||
                  enfermeroId === null
                }
              >
                {guardando ? "Guardando..." : "Guardar"}
              </BtnPrimary>

              <button
                type="button"
                className="rounded bg-gray-200 px-4 py-2"
                onClick={() => {
                  setMostrarForm(false);
                  setError("");
                }}
                disabled={guardando}
              >
                Cancelar
              </button>
            </div>
          </div>
        </Panel>
      )}
    </div>
  );
}