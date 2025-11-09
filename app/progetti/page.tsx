export default function ProgettiPage() {
  const progetti = [
    {
      titolo: "Portfolio Personale",
      descrizione: "Sito portfolio con Next.js 15, Tailwind CSS e TypeScript. Blog integrato con MDX per articoli tecnici.",
      tecnologie: ["Next.js", "TypeScript", "Tailwind CSS", "MDX"],
      link: "https://github.com/a-colavito",
      anno: "2025"
    },
    {
      titolo: "Sistema di Gestione",
      descrizione: "Applicazione web per la gestione di progetti e task con autenticazione e dashboard interattiva.",
      tecnologie: ["React", "Node.js", "PostgreSQL", "Express"],
      link: "#",
      anno: "2024"
    },
    {
      titolo: "App Mobile",
      descrizione: "Applicazione mobile cross-platform per il tracking di attività sportive con GPS e statistiche.",
      tecnologie: ["React Native", "Firebase", "Maps API"],
      link: "#",
      anno: "2024"
    }
  ]

  return (
    <section>
      <h1 className="font-semibold text-xl sm:text-2xl mb-6 sm:mb-8 tracking-tighter">
        Progetti
      </h1>
      
      <p className="mb-6 sm:mb-8 text-sm sm:text-base text-neutral-700 dark:text-neutral-300">
        Una selezione di progetti su cui ho lavorato, sperimentando con diverse 
        tecnologie e affrontando sfide interessanti.
      </p>

      <div className="space-y-6 sm:space-y-8">
        {progetti.map((progetto, index) => (
          <div 
            key={index}
            className="border border-neutral-200 dark:border-neutral-800 rounded-lg p-4 sm:p-6 hover:border-neutral-300 dark:hover:border-neutral-700 transition-colors"
          >
            <div className="flex flex-col sm:flex-row sm:justify-between sm:items-start mb-3 gap-1">
              <h2 className="font-semibold text-lg sm:text-xl tracking-tight">
                {progetto.titolo}
              </h2>
              <span className="text-xs sm:text-sm text-neutral-500 dark:text-neutral-400">
                {progetto.anno}
              </span>
            </div>
            
            <p className="text-sm sm:text-base text-neutral-700 dark:text-neutral-300 mb-4">
              {progetto.descrizione}
            </p>
            
            <div className="flex flex-wrap gap-2 mb-4">
              {progetto.tecnologie.map((tech, i) => (
                <span 
                  key={i}
                  className="px-2 sm:px-3 py-1 text-xs sm:text-sm bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 rounded-full"
                >
                  {tech}
                </span>
              ))}
            </div>
            
            {progetto.link !== "#" && (
              <a 
                href={progetto.link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs sm:text-sm text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 underline"
              >
                Vedi su GitHub →
              </a>
            )}
          </div>
        ))}
      </div>

      <div className="mt-8 sm:mt-12 p-4 sm:p-6 bg-neutral-50 dark:bg-neutral-900 rounded-lg border border-neutral-200 dark:border-neutral-800">
        <h3 className="font-semibold text-base sm:text-lg mb-2">Hai un progetto in mente?</h3>
        <p className="text-sm sm:text-base text-neutral-700 dark:text-neutral-300 mb-4">
          Sono sempre interessato a collaborare su progetti stimolanti o a discutere di nuove idee.
        </p>
        <a 
          href="/contatti"
          className="inline-block px-4 py-2 text-sm sm:text-base bg-neutral-900 dark:bg-neutral-100 text-white dark:text-neutral-900 rounded-lg hover:bg-neutral-800 dark:hover:bg-neutral-200 transition-colors font-medium"
        >
          Contattami
        </a>
      </div>
    </section>
  )
}
