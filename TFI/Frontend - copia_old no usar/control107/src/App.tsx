// src/App.tsx
import { BrowserRouter, Routes, Route } from "react-router-dom";

// Páginas
import Login from "./pages/Login";
import Home from "./pages/Home";
import OperativoEnfermero from "./pages/OperativoEnfermero";

import AdminUsuarios from "./pages/AdminUsuarios";
import AdminAmbulancias from "./pages/AdminAmbulancias";
import AdminInsumos from "./pages/AdminInsumos";
import AdminTurnos from "./pages/AdminTurnos";
import AdminHistorial from "./pages/AdminHistorial";
import AdminDashboard from "./pages/AdminDashboard";

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-fondo font-plex text-petro">

        <Routes>
          {/* Login */}
          <Route path="/" element={<Login />} />

          <Route path="/home" element={<Home />} />

          {/* Enfermero */}
          <Route path="/operativo" element={<OperativoEnfermero />} />

          {/* Administración */}
          <Route path="/admin/usuarios" element={<AdminUsuarios />} />
          <Route path="/admin/ambulancias" element={<AdminAmbulancias />} />
          <Route path="/admin/insumos" element={<AdminInsumos />} />
          <Route path="/admin/turnos" element={<AdminTurnos />} />
          <Route path="/admin/historial" element={<AdminHistorial />} />
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
        </Routes>

      </div>
    </BrowserRouter>
  );
}
