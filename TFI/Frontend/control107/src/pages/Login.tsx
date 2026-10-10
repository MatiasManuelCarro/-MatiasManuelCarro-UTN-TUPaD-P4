// import { useState } from "react";

// export default function Login() {
//   const [email, setEmail] = useState("");
//   const [pass, setPass] = useState("");

//   return (
    
//     <div className="min-h-screen bg-fondo flex items-center justify-center">
//       <div className="bg-blanco p-8 rounded-lg shadow-md w-90">
//         <h1 className="text-2xl font-barlow text-petro mb-6 text-center">
//           107 Control
//         </h1>

//         <div className="flex flex-col gap-4">
//           <div className="flex flex-col gap-1">
//             <label className="font-barlow text-petro">Email</label>
//             <input
//               type="email"
//               value={email}
//               onChange={(e) => setEmail(e.target.value)}
//               className="border border-fondo p-3 rounded font-plex focus:outline-none focus:ring-2 focus:ring-turquesa"
//             />
//           </div>

//           <div className="flex flex-col gap-1">
//             <label className="font-barlow text-petro">Contraseña</label>
//             <input
//               type="password"
//               value={pass}
//               onChange={(e) => setPass(e.target.value)}
//               className="border border-fondo p-3 rounded font-plex focus:outline-none focus:ring-2 focus:ring-turquesa"
//             />
//           </div>

//           <button className="bg-turquesa text-white font-plex py-3 rounded hover:bg-petro transition">
//             Ingresar
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// }

// import { useState } from "react";

// export default function Login() {
//   const [email, setEmail] = useState("");
//   const [pass, setPass] = useState("");
//   const [error, setError] = useState("");

//   async function handleLogin() {
//     setError("");

//     try {
//       const res = await fetch("http://localhost:3000/auth/login", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ email, password: pass }),
//       });

//       if (!res.ok) {
//         setError("Credenciales incorrectas");
//         return;
//       }

//       const data = await res.json();

//       // Guardar token
//       localStorage.setItem("token", data.token);

//       // Redirigir
//       window.location.href = "/home";
//     } catch (err) {
//       setError("Error de conexión con el servidor");
//     }
//   }

//   return (
//     <div className="min-h-screen bg-fondo flex items-center justify-center">
//       <div className="bg-blanco p-8 rounded-lg shadow-md w-[360px]">
//         <h1 className="text-2xl font-barlow text-petro mb-6 text-center">
//           107 Control
//         </h1>

//         <div className="flex flex-col gap-4">
//           {error && (
//             <div className="bg-coral text-white p-2 rounded font-plex text-sm">
//               {error}
//             </div>
//           )}

//           <div className="flex flex-col gap-1">
//             <label className="font-barlow text-petro">Email</label>
//             <input
//               type="email"
//               value={email}
//               onChange={(e) => setEmail(e.target.value)}
//               className="border border-fondo p-3 rounded font-plex focus:outline-none focus:ring-2 focus:ring-turquesa"
//             />
//           </div>

//           <div className="flex flex-col gap-1">
//             <label className="font-barlow text-petro">Contraseña</label>
//             <input
//               type="password"
//               value={pass}
//               onChange={(e) => setPass(e.target.value)}
//               className="border border-fondo p-3 rounded font-plex focus:outline-none focus:ring-2 focus:ring-turquesa"
//             />
//           </div>

//           <button
//             onClick={handleLogin}
//             className="bg-turquesa text-white font-plex py-3 rounded hover:bg-petro transition"
//           >
//             Ingresar
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// }


export default function Login() {
  window.location.href = "/home";
  return null;
}
