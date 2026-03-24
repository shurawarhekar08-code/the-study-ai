// vite.config.js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    // Proxy /api/* → Flask in development so you never hit CORS
    proxy: {
      "/api": {
        target:      "http://localhost:5000",
        changeOrigin: true,
        rewrite:     (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
