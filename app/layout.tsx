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
      <body className="antialiased max-w-2xl mx-auto bg-white dark:bg-black text-black dark:text-white">
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <main className="flex-auto min-w-0 mt-6 flex flex-col px-2 md:px-0">
            <Navbar />
            {children}
            <Footer />
            <Analytics />
            <SpeedInsights />
          </main>
        </ThemeProvider>
      </body>
    </html>
  )
}
