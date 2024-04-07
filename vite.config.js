import { defineConfig, splitVendorChunkPlugin } from 'vite'
import { fileURLToPath, URL } from 'node:url'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { glob } from 'glob'
import Components from 'unplugin-vue-components/vite'
import { AntDesignVueResolver } from 'unplugin-vue-components/resolvers'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    splitVendorChunkPlugin(),
    Components({
      resolvers: [
        AntDesignVueResolver({
          importStyle: false, // css in js
        }),
      ],
    }),
  ],
  base: '/static/',
  root: './calyvim/static',
  build: {
    manifest: 'manifest.json',
    rollupOptions: {
      input: glob.sync(
        path.resolve(__dirname, 'calyvim/static/entrypoints/**/*.js')
      ),
    },
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./calyvim/static', import.meta.url)),
    },
  },
})
