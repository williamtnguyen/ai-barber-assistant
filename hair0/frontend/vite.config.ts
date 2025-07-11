import path from "path"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"
import { viteStaticCopy } from "vite-plugin-static-copy"

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(), 
    tailwindcss(),
    viteStaticCopy({
      targets: [
        {
          src: 'public/*',
          dest: 'static'
        }
      ]
    })
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    // Build to the location where Python server expects files
    outDir: "../src/frontend/build",
    emptyOutDir: true,
    // Ensure assets are referenced correctly
    assetsDir: "static",
    // Don't copy public directory automatically (we handle it with static-copy plugin)
    copyPublicDir: false,
  },
  server: {
    // Development server configuration
    port: 5173,
    host: true,
    // Proxy API requests to Python backend during development
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/health': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
