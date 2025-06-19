import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  experimental: {
    appDir: true, // ? App Router È°¼ºÈ­!
  },
};

export default nextConfig;