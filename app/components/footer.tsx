export default function Footer() {
  return (
    <footer className="mb-8 sm:mb-12 lg:mb-16">
      <p className="mt-6 sm:mt-8 text-sm sm:text-base text-neutral-600 dark:text-neutral-300">
        © {new Date().getFullYear()} Adolfo Colavito
      </p>
      <p className="mt-2 text-xs sm:text-sm text-neutral-500 dark:text-neutral-400">
        Basato sul{' '}
        <a 
          href="https://vercel.com/templates/next.js/nextjs-portfolio" 
          target="_blank" 
          rel="noopener noreferrer"
          className="hover:text-neutral-700 dark:hover:text-neutral-200 transition-colors underline break-words"
        >
          Next.js Portfolio Template
        </a>
        {' '}di Vercel
      </p>
    </footer>
  )
}
