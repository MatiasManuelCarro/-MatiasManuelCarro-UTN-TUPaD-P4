import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import CategoriasPage from "./pages/CategoriasPage";

export default function App() {
  return (
    <>
      <div className="min-h-screen flex flex-col">
        <Navbar />

        <main className="flex-1 p-4 bg-slate-50">
          <CategoriasPage />
        </main>

        <Footer />
      </div>
    </>
  );
}