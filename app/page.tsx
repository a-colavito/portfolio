import { BlogPosts } from 'app/components/posts'
import Image from 'next/image'
import Link from 'next/link'

export default function Page() {
  return (
    <section>
      {/* Business Card Hero */}
      <div className="mb-20">
        <Link href="/contatti" className="block">
          <div className="p-6 sm:p-8 lg:p-10 rounded-2xl border border-neutral-200 dark:border-neutral-800 bg-gradient-to-br from-neutral-50 to-white dark:from-neutral-900 dark:to-black hover:border-neutral-400 dark:hover:border-neutral-600 transition-all duration-300 cursor-pointer group">
            <div className="flex gap-4 sm:gap-6 lg:gap-8 items-center">
              <div className="relative aspect-square w-32 sm:w-28 md:w-32 lg:w-36 xl:w-40 rounded-full overflow-hidden flex-shrink-0 border border-neutral-200 dark:border-neutral-700 group-hover:border-neutral-400 dark:group-hover:border-neutral-500 transition-colors">
                <Image
                  src="https://res.cloudinary.com/dkkvkj82k/image/upload/v1762627002/7IV01608_hmvipl.jpg"
                  alt="Adolfo Colavito"
                  fill
                  className="object-cover grayscale group-hover:grayscale-0 transition-all duration-500"
                  priority
                  sizes="(max-width: 640px) 128px, (max-width: 768px) 112px, (max-width: 1024px) 128px, (max-width: 1280px) 144px, 160px"
                />
              </div>
              
              <div className="flex-1 min-w-0">
                <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold tracking-tight mb-2">
                  Adolfo Colavito
                </h1>
                <p className="text-base sm:text-lg text-neutral-600 dark:text-neutral-400 mb-3">
                  Ingegnere informatico, studente, runner
                </p>
                <p className="text-sm text-neutral-600 dark:text-neutral-400 leading-relaxed">
                  Studente al Politecnico di Bari. Appassionato di tecnologia, codice, 
                  running e Radiohead. Qui condivido pensieri su web development e algoritmi.
                </p>
              </div>
            </div>
          </div>
        </Link>
      </div>

      {/* Blog Posts Section */}
      <div>
        <h2 className="mb-8 text-2xl font-semibold tracking-tight">
          Ultimi articoli
        </h2>
        <BlogPosts limit={5} />
      </div>
    </section>
  )
}
