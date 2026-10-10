// import { useEffect, useState } from "react";

// export default function AdminInsumos() {
//   const [insumos, setInsumos] = useState<any[]>([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState("");

//   useEffect(() => {
//     Promise.all([
//       fetch("http://localhost:8000/insumos").then((r) => r.json()),
//       fetch("http://localhost:8000/categorias").then((r) => r.json()),
//     ])
//       .then(([insumosData, categoriasData]) => {
//         console.log("INSUMOS:", insumosData);
//         console.log("CATEGORIAS:", categoriasData);

//         // unir insumos con categorías
//         const insumosConCategoria = insumosData.map((i: any) => {
//           const categoria = categoriasData.find(
//             (c: any) => c.id === i.categoria_id
//           );

//           return {
//             ...i,
//             categoria_nombre: categoria ? categoria.nombre : "Sin categoría",
//             categoria_color: categoria ? categoria.color : "#999999",
//           };
//         });

//         setInsumos(insumosConCategoria);
//       })
//       .catch((err) => {
//         console.log("ERROR FETCH:", err);
//         setError("No se pudo cargar insumos o categorías");
//       })
//       .finally(() => setLoading(false));
//   }, []);

//   if (loading) {
//     return <div className="p-10 text-petro">Cargando insumos...</div>;
//   }

//   if (error) {
//     return (
//       <div className="p-10">
//         <div className="bg-coral text-white p-4 rounded font-plex">
//           {error}
//         </div>
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen bg-fondo p-10 font-plex text-petro">
//       <h1 className="text-3xl font-barlow mb-8">Insumos</h1>

//       <ul className="flex flex-col gap-4">
//         {insumos.map((i) => (
//           <li
//             key={i.id}
//             className="bg-blanco p-6 rounded-lg shadow border border-fondo"
//           >
//             <h2 className="text-xl font-barlow mb-2">{i.nombre}</h2>

//             <p className="text-sm text-petro mb-2">
//               Punto de control: <span className="font-bold">{i.punto_control}</span>
//             </p>

//             {/* Categoría con color */}
//             <div className="flex items-center gap-2 mb-4">
//               <span
//                 className="inline-block w-4 h-4 rounded-full"
//                 style={{ backgroundColor: i.categoria_color }}
//               ></span>
//               <span className="text-sm font-bold text-azul">
//                 {i.categoria_nombre}
//               </span>
//             </div>

//             <CriticoBadge critico={i.critico} />

//             <div className="mt-4">
//               <button className="bg-turquesa text-white px-4 py-2 rounded hover:bg-petro transition">
//                 Ver detalles
//               </button>
//             </div>
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// }

// function CriticoBadge({ critico }: { critico: boolean }) {
//   const estado = critico ? "Crítico" : "Normal";
//   const color = critico ? "bg-coral" : "bg-verde";

//   return (
//     <span
//       className={`${color} text-white px-3 py-1 rounded font-barlow text-sm`}
//     >
//       {estado}
//     </span>
//   );
// }


import { useEffect, useState } from "react";

export default function AdminInsumos() {
  const [insumos, setInsumos] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      fetch("http://localhost:8000/insumos").then((r) => r.json()),
      fetch("http://localhost:8000/categorias").then((r) => r.json()),
    ])
      .then(([insumosData, categoriasData]) => {
        const insumosConCategoria = insumosData.map((i: any) => {
          const categoria = categoriasData.find((c: any) => c.id === i.categoria_id);

          return {
            ...i,
            categoria_nombre: categoria?.nombre ?? "Sin categoría",
            categoria_color: categoria?.color ?? "#999999",
          };
        });

        setInsumos(insumosConCategoria);
      })
      .catch(() => setError("No se pudo cargar insumos o categorías"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-10 text-petro animate-pulse">Cargando insumos...</div>;
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
      <div className="w-full max-w-4xl">
        <h1 className="text-4xl font-barlow mb-10 tracking-tight">Insumos</h1>

        <ul className="flex flex-col gap-6">
          {insumos.map((i) => (
            <li
              key={i.id}
              className="
                bg-white p-6 rounded-xl shadow-md border border-gray-100
                hover:shadow-xl hover:-translate-y-1 transition-all duration-300
              "
            >
              <div className="flex justify-between items-start">
                <h2 className="text-2xl font-barlow mb-3">{i.nombre}</h2>
                <CriticoBadge critico={i.critico} />
              </div>

              <p className="text-sm text-petro/80 mb-4">
                Punto de control: <span className="font-bold text-petro">{i.punto_control}</span>
              </p>

              <div className="flex items-center gap-3 mb-6">
                <span
                  className="inline-block w-5 h-5 rounded-full shadow-sm"
                  style={{ backgroundColor: i.categoria_color }}
                ></span>
                <span className="text-sm font-semibold text-azul tracking-wide">
                  {i.categoria_nombre}
                </span>
              </div>

              <button
                className="
                  bg-turquesa text-white px-5 py-2.5 rounded-lg
                  hover:bg-petro transition-colors duration-300
                  font-barlow shadow-sm
                "
              >
                Ver detalles
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

function CriticoBadge({ critico }: { critico: boolean }) {
  const estado = critico ? "Crítico" : "Normal";
  const color = critico ? "bg-coral" : "bg-verde";

  return (
    <span
      className={`
        ${color} text-white px-3 py-1.5 rounded-md font-barlow text-xs
        shadow-sm tracking-wide
      `}
    >
      {estado}
    </span>
  );
}
