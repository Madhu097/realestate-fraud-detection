import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        react({
            jsxRuntime: 'automatic',
        }),
        tailwindcss(),
    ],
    server: {
        port: 5173,
        strictPort: true,
        host: true,
        cors: true,
        // Proxy disabled for production - using VITE_API_BASE_URL env variable instead
    }
})
