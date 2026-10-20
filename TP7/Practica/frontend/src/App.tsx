import { Navbar } from "./components/Navbar";
import ProductsPage from "./pages/ProductsPage";
import CategoriasPage from "./pages/CategoriasPage";
import { Route, Routes } from "react-router-dom";
import { Footer } from "./components/Footer";

function App() {
  return (
    <div className="flex min-h-screen flex-col bg-slate-900 text-white">
      <Navbar />
       <main className="flex-1">
            <Routes>
        <Route
          path="/"
          element={<CategoriasPage />}
        />

        <Route
          path="/categorias"
          element={<CategoriasPage />}
        />

        <Route
          path="/productos"
          element={<ProductsPage />}
        />
      </Routes>
      </main>
      <Footer />
    </div>
  );
}

export default App;
