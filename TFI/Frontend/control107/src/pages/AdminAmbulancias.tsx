// import { useEffect, useState } from "react";

// export default function AdminAmbulancias() {
//   const [ambulancias, setAmbulancias] = useState<any[]>([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState("");

//   useEffect(() => {
//     fetch("http://localhost:8000/ambulancias")
//       .then((res) => {
//         if (!res.ok) throw new Error("Error en el servidor");
//         return res.json();
//       })
//       .then((data) => {
//         console.log("AMBULANCIAS:", data);

//         if (Array.isArray(data)) {
//           setAmbulancias(data);
//         } else {
//           setError("Formato inválido en backend");
//         }
//       })
//       .catch((err) => {
//         console.log("ERROR FETCH:", err);
//         setError("No se pudo cargar ambulancias");
//       })
//       .finally(() => setLoading(false));
//   }, []);

//   if (loading) {
//     return <div className="p-10 text-petro">Cargando ambulancias...</div>;
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
//       <h1 className="text-3xl font-barlow mb-8">Dashboard de Ambulancias</h1>

//       {ambulancias.length === 0 && (
//         <p className="text-azul">No hay ambulancias registradas.</p>
//       )}

//       <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
//         {ambulancias.map((a) => (
//           <div
//             key={a.id}
//             className="bg-blanco p-6 rounded-lg shadow border border-fondo"
//           >
//             <h2 className="text-xl font-barlow mb-2">
//               Ambulancia #{a.id}
//             </h2>

//             <p className="text-sm text-petro mb-2">
//               Patente: <span className="font-bold">{a.patente}</span>
//             </p>

//             <EstadoBadge disponible={a.disponible} />

//             <div className="mt-4">
//               <button className="bg-turquesa text-white px-4 py-2 rounded hover:bg-petro transition">
//                 Ver detalles
//               </button>
//             </div>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }

// function EstadoBadge({ disponible }: { disponible: boolean }) {
//   const estado = disponible ? "Disponible" : "No disponible";
//   const color = disponible ? "bg-verde" : "bg-coral";

//   return (
//     <span
//       className={`${color} text-white px-3 py-1 rounded font-barlow text-sm`}
//     >
//       {estado}
//     </span>
//   );
// }


import { useEffect, useState } from "react";

export default function AdminAmbulancias() {
  const [ambulancias, setAmbulancias] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/ambulancias")
      .then((res) => {
        if (!res.ok) throw new Error("Error en el servidor");
        return res.json();
      })
      .then((data) => {
        if (Array.isArray(data)) {
          setAmbulancias(data);
        } else {
          setError("Formato inválido en backend");
        }
      })
      .catch(() => setError("No se pudo cargar ambulancias"))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="p-10 text-petro animate-pulse">Cargando ambulancias...</div>;
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
      <div className="w-full max-w-5xl">
        <h1 className="text-4xl font-barlow mb-10 tracking-tight">
          Ambulancias
        </h1>

        {ambulancias.length === 0 && (
          <p className="text-azul">No hay ambulancias registradas.</p>
        )}

        <ul className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {ambulancias.map((a) => (
            <li
              key={a.id}
              className="
                bg-white p-6 rounded-xl shadow-md border border-gray-100
                hover:shadow-xl hover:-translate-y-1 transition-all duration-300
              "
            >
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-2xl font-barlow">
                  Unidad #{a.id}
                </h2>

                <EstadoBadge disponible={a.disponible} />
              </div>

              <p className="text-sm text-petro/80 mb-6">
                Patente: <span className="font-bold text-petro">{a.patente}</span>
              </p>

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

function EstadoBadge({ disponible }: { disponible: boolean }) {
  const estado = disponible ? "Disponible" : "No disponible";
  const color = disponible ? "bg-verde" : "bg-coral";

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
