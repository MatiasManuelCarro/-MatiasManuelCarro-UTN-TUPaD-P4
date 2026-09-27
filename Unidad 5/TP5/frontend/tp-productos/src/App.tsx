import Header from "./components/Header"
import ProductoForm from "./components/ProductoForm"
import ProductoList from "./components/ProductoList"
import Footer from "./components/Footer"
import type { Producto } from "./types/producto"

export default function App() {
const productos: Producto[] = [
  {
    id: 1,
    nombre: "Mouse Gamer",
    descripcion: "RGB, 12000 DPI",
    precio: 25000
  },
  {
    id: 2,
    nombre: "Teclado Mecánico",
    descripcion: "Switch Red",
    precio: 45000
  },
  {
    id: 3,
    nombre: "Auriculares Inalámbricos",
    descripcion: "Bluetooth 5.3",
    precio: 38000
  },
  {
    id: 4,
    nombre: "Monitor 24'' IPS",
    descripcion: "1080p, 75Hz",
    precio: 95000
  },
  {
    id: 5,
    nombre: "Silla Ergonómica",
    descripcion: "Altura regulable, soporte lumbar",
    precio: 120000
  },
  {
    id: 6,
    nombre: "Webcam Full HD",
    descripcion: "1080p, micrófono integrado",
    precio: 30000
  },
  {
    id: 7,
    nombre: "Parlantes 2.1",
    descripcion: "Subwoofer, 40W RMS",
    precio: 42000
  },
  {
    id: 8,
    nombre: "SSD NVMe 1TB",
    descripcion: "PCIe 3.0, lectura 3500MB/s",
    precio: 55000
  },
  {
    id: 9,
    nombre: "Router WiFi 6",
    descripcion: "Dual band, 1800 Mbps",
    precio: 52000
  },
  {
    id: 10,
    nombre: "Impresora Multifunción",
    descripcion: "Escáner + WiFi",
    precio: 85000
  }
]


  return (
    <div className="flex min-h-screen flex-col bg-slate-100 justify-between">
      <Header />

      <main className="mx-auto flex w-full max-w-4xl flex-col gap-8 px-4 py-8">
        <ProductoForm />
        <ProductoList productos={productos} />
      </main>

      <Footer />
    </div>
  )
}