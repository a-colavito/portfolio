import { Projects } from 'app/components/projects'

export const metadata = {
  title: 'Progetti',
  description: 'Progetti su cui ho lavorato, sperimentando con diverse tecnologie.',
}

export default function ProgettiPage() {
  return (
    <section>
      <h1 className="font-semibold text-2xl mb-8 tracking-tighter">
        Progetti
      </h1>
      
      <p className="mb-8 text-neutral-700 dark:text-neutral-300">
        Una selezione di progetti su cui ho lavorato, sperimentando con diverse 
        tecnologie e affrontando sfide interessanti.
      </p>

      <Projects />

      <div className="mt-12 p-6 bg-neutral-50 dark:bg-neutral-900 rounded-lg border border-neutral-200 dark:border-neutral-800">
        <h3 className="font-semibold text-lg mb-2">Hai un progetto in mente?</h3>
        <p className="text-neutral-700 dark:text-neutral-300 mb-4">
          Sono sempre interessato a collaborare su progetti stimolanti o a discutere di nuove idee.
        </p>
        <a 
          href="/contatti"
          className="inline-block px-4 py-2 bg-neutral-900 dark:bg-neutral-100 text-white dark:text-neutral-900 rounded-lg hover:bg-neutral-800 dark:hover:bg-neutral-200 transition-colors font-medium"
        >
          Contattami
        </a>
      </div>
    </section>
  )
}
