import { useEffect, useState } from "react";
import { Panel } from "../components/Panel";
import { BtnPrimary } from "../components/Base/BtnPrimary";
import { listarTurnos, crearTurno } from "../services/turnos";
import { listarAmbulancias } from "../services/ambulancias";
import { listarEnfermerosActivos } from "../services/enfermeros";

export default function AdminTurnos() {
  const [turnos, setTurnos] = useState([]);
  const [mostrarForm, setMostrarForm] = useState(false);

  const [fecha, setFecha] = useState("");
  const [horario, setHorario] = useState("MANIANA");

  const [ambulancias, setAmbulancias] = useState([]);
  const [ambulanciaId, setAmbulanciaId] = useState(1);

  const [enfermeros, setEnfermeros] = useState([]);
  const [enfermeroId, setEnfermeroId] = useState(2);

  const [chofer, setChofer] = useState("");

  const [medico, setMedico] = useState("");


  useEffect(() => {
    listarTurnos().then(setTurnos)
    listarAmbulancias().then(setAmbulancias);
    listarEnfermerosActivos().then(setEnfermeros);
  }, []);

const handleCrear = () => {
  crearTurno({
    fecha,
    horario,
    estado: "PROGRAMADO",
    nombreChofer: chofer,
    nombreMedico: medico,
    ambulanciaId,
    enfermeroId,
    adminId: 1
  }).then(() => {
    listarTurnos().then(setTurnos);
    setMostrarForm(false);
  });
};



  return (
    <div className="p-6 space-y-6 bg-fondo min-h-screen">
      <h1 className="font-barlow text-3xl text-petro">Turnos</h1>

      <Panel title="Programación">
        <div className="space-y-4">
          {turnos.map((t: any) => (
            <div
              key={t.id}
              className="p-4 bg-blanco border rounded flex justify-between"
            >
              <span className="font-plex text-petro">
                {t.fecha} – {t.horario}
              </span>
              <span className="font-mono text-azul">{t.estado}</span>
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
              <label className="font-barlow text-petro">Fecha</label>
              <input
                type="date"
                className="border p-2 rounded"
                value={fecha}
                onChange={(e) => setFecha(e.target.value)}
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="font-barlow text-petro">Horario</label>
              <select
                className="border p-2 rounded"
                value={horario}
                onChange={(e) => setHorario(e.target.value)}
              >
                <option value="MANIANA">Mañana</option>
                <option value="TARDE">Tarde</option>
                <option value="NOCHE">Noche</option>
              </select>
            </div>

            <div className="flex flex-col gap-2">
              <label className="font-barlow text-petro">Ambulancia</label>
              <select
                className="border p-2 rounded"
                value={ambulanciaId}
                onChange={(e) => setAmbulanciaId(Number(e.target.value))}
              >
                {ambulancias.map((a: any) => (
                  <option key={a.id} value={a.id}>
                    {a.nombre ?? `Ambulancia ${a.id}`}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex flex-col gap-2">
              <label className="font-barlow text-petro">Conductor</label>
              <input
                type="text"
                className="border p-2 rounded"
                value={chofer}
                onChange={(e) => setChofer(e.target.value)}
                placeholder="Nombre del chofer"
              />
            </div>

            <div className="flex flex-col gap-2">
              <label className="font-barlow text-petro">Médico</label>
              <input
                type="text"
                className="border p-2 rounded"
                value={medico}
                onChange={(e) => setMedico(e.target.value)}
                placeholder="Nombre del médico"
              />
            </div>


            <div className="flex flex-col gap-2">
              <label className="font-barlow text-petro">Enfermero</label>
              <select
                className="border p-2 rounded"
                value={enfermeroId}
                onChange={(e) => setEnfermeroId(Number(e.target.value))}
              >
                {enfermeros.map((u: any) => (
                  <option key={u.id} value={u.id}>
                    {u.nombre}
                  </option>
                ))}
              </select>
            </div>



            <BtnPrimary onClick={handleCrear}>Guardar</BtnPrimary>
          </div>
        </Panel>
      )}
    </div>
  );
}
