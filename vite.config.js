import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  base: '/',
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  input: {
    index: resolve(__dirname, './index.html'), // Path to your main index.html
    events: resolve(__dirname, './public/events.html'), // Path to your events.html
    about: resolve(__dirname, './public/about.html'), // Path to your about.html
  },
})