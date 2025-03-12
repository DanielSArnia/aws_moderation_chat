import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  define: {
    global: 'window', // This tells Vite to use `window` in place of `global`
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
})
