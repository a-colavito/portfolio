import './global.css'
import type { Metadata } from 'next'
import { GeistSans } from 'geist/font/sans'
import { GeistMono } from 'geist/font/mono'
import { Navbar } from './components/nav'
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/next'
import Footer from './components/footer'
import { baseUrl } from './sitemap'
import { ThemeProvider } from 'next-themes'

export const metadata: Metadata = {
  metadataBase: new URL(baseUrl),
  title: {
    default: 'Adolfo Colavito - Ingegnere Informatico',
    template: '%s | Adolfo Colavito',
  },
  description: 'Studente di Ingegneria Informatica al Politecnico di Bari. Blog su web development, algoritmi, tecnologia e running.',
  keywords: ['Adolfo Colavito', 'Ingegnere Informatico', 'Web Development', 'Politecnico di Bari', 'Blog', 'Programmazione', 'Runner'],
  authors: [{ name: 'Adolfo Colavito', url: 'https://github.com/a-colavito' }],
  creator: 'Adolfo Colavito',
  openGraph: {
    title: 'Adolfo Colavito - Ingegnere Informatico',
    description: 'Studente di Ingegneria Informatica al Politecnico di Bari. Blog su web development, algoritmi, tecnologia e running.',
    url: baseUrl,
    siteName: 'Adolfo Colavito',
    locale: 'it_IT',
    type: 'website',
    images: [
      {
        url: 'https://res.cloudinary.com/dkkvkj82k/image/upload/v1762627002/7IV01608_hmvipl.jpg',
        width: 1200,
        height: 630,
        alt: 'Adolfo Colavito',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Adolfo Colavito - Ingegnere Informatico',
    description: 'Studente di Ingegneria Informatica al Politecnico di Bari. Blog su web development, algoritmi, tecnologia e running.',
    images: ['https://res.cloudinary.com/dkkvkj82k/image/upload/v1762627002/7IV01608_hmvipl.jpg'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}

const cx = (...classes) => classes.filter(Boolean).join(' ')

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html
      lang="it"
      className={cx(
        GeistSans.variable,
        GeistMono.variable
      )}
      suppressHydrationWarning
    >
      <body className="antialiased bg-white dark:bg-black text-black dark:text-white transition-colors duration-200">
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <div className="flex flex-col min-h-screen">
            <div className="max-w-2xl lg:max-w-4xl xl:max-w-5xl mx-auto px-4 md:px-6 lg:px-8 py-8 flex-grow w-full">
              <Navbar />
              <main className="mt-6">
                {children}
              </main>
            </div>
            <div className="max-w-2xl lg:max-w-4xl xl:max-w-5xl mx-auto px-4 md:px-6 lg:px-8 w-full">
              <Footer />
            </div>
          </div>
          <Analytics />
          <SpeedInsights />
        </ThemeProvider>
      </body>
    </html>
  )
}
