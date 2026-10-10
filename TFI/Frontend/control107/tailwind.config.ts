import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        // Identidad base
        petro: "#17313B",        // Azul petróleo · Base
        turquesa: "#087E8B",     // Acción
        coral: "#D9574C",        // Crítico
        ambar: "#D99A18",        // Revisar
        verde: "#2A9D72",        // Completo
        azul: "#3978A8",         // Información

        // Superficies
        fondo: "#F3F7F6",        // Respiración
        blanco: "#FFFFFF",       // Superficie
      },

      fontFamily: {
        barlow: ["Barlow Semi Condensed", "sans-serif"],
        plex: ["IBM Plex Sans", "sans-serif"],
        mono: ["IBM Plex Mono", "monospace"],
      },
    },
  },
} satisfies Config;
