import { defineConfig } from "astro/config";

// Static output only: pages are built from published JSON, nothing is rendered per request.
export default defineConfig({
  output: "static",
  trailingSlash: "always",
});
