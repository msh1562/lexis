import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  experimental: {
    appDir: true, // ? App Router Ȱ��ȭ!
  },
};

export default nextConfig;