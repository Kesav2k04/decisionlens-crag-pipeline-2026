import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// In dev, proxy /api to the FastAPI service so the SPA uses same-origin URLs
// (matching a production deploy where both are served behind one origin).
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': { target: 'http://127.0.0.1:8077', changeOrigin: true },
    },
  },
  build: {
    target: 'es2020',
    sourcemap: true,
    // Don't inject <link rel="modulepreload"> for async chunks. Vite's
    // automatic splitting already isolates Three.js behind the lazy Scene3D
    // import; a manual chunk for it would make the entry depend on it eagerly,
    // so we deliberately let automatic splitting keep it on-demand only.
    modulePreload: false,
  },
})
