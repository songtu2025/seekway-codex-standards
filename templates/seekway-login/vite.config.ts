import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { readFileSync } from "node:fs";

export default defineConfig({
  plugins: [
    react(),
    {
      name: "font-license",
      generateBundle() {
        // 字体许可随构建产物分发，不能只留在源码中。
        this.emitFile({
          type: "asset",
          fileName: "Fonts-LICENSE.txt",
          source: readFileSync(
            new URL("./src/assets/Fonts-LICENSE.txt", import.meta.url),
            "utf8",
          ),
        });
      },
    },
  ],
  base: "./",
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (/node_modules[/\\](react|react-dom|scheduler)[/\\]/.test(id))
            return "react";
          if (id.includes("node_modules")) return "antd";
        },
      },
    },
  },
});
