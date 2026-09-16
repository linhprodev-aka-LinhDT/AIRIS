import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    cssMinify: false,
  },
  server: {
    port: 5173,
    host: 'airis.local',
    allowedHosts: ['airis.local'],
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
  preview: {
    port: 4173,
    host: 'airis.local',
  },
});
