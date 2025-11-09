import { BlogPosts } from 'app/components/posts'
import Image from 'next/image'
import Link from 'next/link'

export default function Page() {
  return (
    <section>
      {/* Business Card Hero */}
      <div className="mb-20">
        <Link href="/contatti" className="block">
          <div className="p-6 rounded-2xl border border-neutral-200 dark:border-neutral-800 bg-gradient-to-br from-neutral-50 to-white dark:from-neutral-900 dark:to-black hover:border-neutral-400 dark:hover:border-neutral-600 transition-all duration-300 cursor-pointer group">
            <div className="flex flex-col sm:flex-row gap-6 items-center sm:items-start">
              <div className="relative aspect-square w-32 rounded-full overflow-hidden flex-shrink-0 border border-neutral-200 dark:border-neutral-700 group-hover:border-neutral-400 dark:group-hover:border-neutral-500 transition-colors">
                <Image
                  src="https://res.cloudinary.com/dkkvkj82k/image/upload/v1762627002/7IV01608_hmvipl.jpg"
                  alt="Adolfo Colavito"
                  fill
                  className="object-cover grayscale group-hover:grayscale-0 transition-all duration-500"
                  priority
                  sizes="128px"
                />
              </div>
              
              <div className="flex-1 text-center sm:text-left">
                <h1 className="text-2xl font-bold tracking-tight mb-2">
                  Adolfo Colavito
                </h1>
                <p className="text-neutral-600 dark:text-neutral-400 mb-3">
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
