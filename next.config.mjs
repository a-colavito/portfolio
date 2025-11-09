/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  basePath: process.env.PAGES_BASE_PATH,
  images: {
    unoptimized: true,
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'res.cloudinary.com',
      },
    ],
  },
}

export default nextConfig
