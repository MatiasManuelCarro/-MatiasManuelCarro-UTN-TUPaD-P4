import Footer from "./components/Footer";
import Navbar from "./components/Navbar";
import TurnoForm from "./components/TurnoForm";
import TurnoList from "./components/TurnoList";
import type { Turno } from "./types/turno";

// Datos hardcodeados: la pantalla es solo maquetado, no consulta la API.
const turnos: Turno[] = [
  {
    id: 1,
    fecha: "2026-09-15",
    hora: "09:30",
    profesional: "Dra. Lopez",
    motivo: "Control anual",
    estado: "confirmado",
    paciente: {
      id: 1,
      nombre: "Ana",
      apellido: "Gomez",
      dni: "30123456",
      telefono: "2614567890",
    },
  },
  {
    id: 2,
    fecha: "2026-09-15",
    hora: "11:00",
    profesional: "Dr. Perez",
    motivo: "Dolor lumbar",
    estado: "pendiente",
    paciente: {
      id: 2,
      nombre: "Carlos",
      apellido: "Diaz",
      dni: "28987654",
      telefono: "2615551234",
    },
  },
  {
    id: 3,
    fecha: "2026-09-16",
    hora: "08:15",
    profesional: "Dra. Lopez",
    motivo: "Renovacion de receta",
    estado: "atendido",
    paciente: {
      id: 3,
      nombre: "Lucia",
      apellido: "Fernandez",
      dni: "35456789",
      telefono: "2613334455",
    },
  },
  {
    id: 4,
    fecha: "2026-09-17",
    hora: "16:45",
    profesional: "Dr. Suarez",
    motivo: "Consulta dermatologica",
    estado: "cancelado",
    paciente: {
      id: 4,
      nombre: "Martin",
      apellido: "Rojas",
      dni: "33112233",
      telefono: "2617778899",
    },
  },
];

function App() {
  return (
    <div className="flex min-h-screen flex-col bg-slate-100 justify-between">
      <Navbar />

      <main className="mx-auto flex w-full max-w-4xl flex-col gap-8 px-4 py-8">
        <TurnoForm />
        <TurnoList turnos={turnos} />
      </main>

      <Footer />
    </div>
  );
}

export default App;
