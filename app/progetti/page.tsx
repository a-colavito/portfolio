export default function ProgettiPage() {
  const progetti = [
    {
      titolo: "Example Project 1",
      descrizione: "A sample project showcasing modern web technologies and best practices.",
      tecnologie: ["React", "TypeScript", "Tailwind CSS"],
      link: "#",
      anno: "2024"
    },
    {
      titolo: "Example Project 2",
      descrizione: "Another example project demonstrating full-stack development skills.",
      tecnologie: ["Next.js", "Node.js", "PostgreSQL"],
      link: "#",
      anno: "2024"
    },
    {
      titolo: "Example Project 3",
      descrizione: "A third example project showing mobile development capabilities.",
      tecnologie: ["React Native", "Firebase"],
      link: "#",
      anno: "2023"
    }
  ]

  return (
    <section>
      <h1 className="font-semibold text-2xl mb-8 tracking-tighter">
        Projects
      </h1>
      
      <p className="mb-8 text-neutral-700 dark:text-neutral-300">
        A selection of projects I've worked on, experimenting with different 
        technologies and tackling interesting challenges.
      </p>

      <div className="space-y-8">
        {progetti.map((progetto, index) => (
          <div 
            key={index}
            className="border border-neutral-200 dark:border-neutral-800 rounded-lg p-6 hover:border-neutral-300 dark:hover:border-neutral-700 transition-colors"
          >
            <div className="flex justify-between items-start mb-3">
              <h2 className="font-semibold text-xl tracking-tight">
                {progetto.titolo}
              </h2>
              <span className="text-sm text-neutral-500 dark:text-neutral-400">
                {progetto.anno}
              </span>
            </div>
            
            <p className="text-neutral-700 dark:text-neutral-300 mb-4">
              {progetto.descrizione}
            </p>
            
            <div className="flex flex-wrap gap-2 mb-4">
              {progetto.tecnologie.map((tech, i) => (
                <span 
                  key={i}
                  className="px-3 py-1 text-sm bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 rounded-full"
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
                className="text-sm text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 underline"
              >
                View on GitHub →
              </a>
            )}
          </div>
        ))}
      </div>

      <div className="mt-12 p-6 bg-neutral-50 dark:bg-neutral-900 rounded-lg border border-neutral-200 dark:border-neutral-800">
        <h3 className="font-semibold text-lg mb-2">Have a project in mind?</h3>
        <p className="text-neutral-700 dark:text-neutral-300 mb-4">
          I'm always interested in collaborating on exciting projects or discussing new ideas.
        </p>
        <a 
          href="/contatti"
          className="inline-block px-4 py-2 bg-neutral-900 dark:bg-neutral-100 text-white dark:text-neutral-900 rounded-lg hover:bg-neutral-800 dark:hover:bg-neutral-200 transition-colors font-medium"
        >
          Get in touch
        </a>
      </div>
    </section>
  )
}
