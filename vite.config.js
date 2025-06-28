import { fileURLToPath, URL } from 'node:url'
import { resolve } from 'node:path'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

const root = resolve(__dirname, 'src')
const outDir = resolve(__dirname, 'dist')

// https://vite.dev/config/
export default defineConfig({
  base: "/dea/",
  root,
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  build: {
    outDir,
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(root, 'index.html'),
        about: resolve(root, 'about', 'index.html'),
        event_list: resolve(root, 'event_list', 'index.html'),
        event_detail: resolve(root, 'event_detail', 'index.html'),
        event_group_detail: resolve(root, 'event_group_detail', 'index.html'),
        circle_participation: resolve(root, 'circle_participation', 'index.html'),
      }
    }
  }
})
