import Link from 'next/link'
import { getProjects } from '../progetti/utils'

export function Projects({ limit }: { limit?: number }) {
  let allProjects = getProjects()

  // Ordina per data (più recenti prima)
  allProjects.sort((a, b) => {
    if (new Date(a.metadata.publishedAt) > new Date(b.metadata.publishedAt)) {
      return -1
    }
    return 1
  })

  // Limita il numero di progetti se specificato
  const projects = limit ? allProjects.slice(0, limit) : allProjects

  return (
    <div className="space-y-6">
      {projects.map((project) => (
        <Link
          key={project.slug}
          className="block group"
          href={`/progetti/${project.slug}`}
        >
          <div className="border border-neutral-200 dark:border-neutral-800 rounded-lg p-6 hover:border-neutral-300 dark:hover:border-neutral-700 transition-colors">
            <div className="flex flex-col md:flex-row md:justify-between md:items-start mb-3 gap-1">
              <h2 className="font-semibold text-xl tracking-tight group-hover:text-neutral-600 dark:group-hover:text-neutral-400 transition-colors">
                {project.metadata.title}
              </h2>
              <span className="text-sm text-neutral-500 dark:text-neutral-400 tabular-nums">
                {new Date(project.metadata.publishedAt).getFullYear()}
              </span>
            </div>
            
            <p className="text-sm text-neutral-700 dark:text-neutral-300 mb-4">
              {project.metadata.summary}
            </p>
            
            <div className="flex flex-wrap gap-2">
              {project.metadata.technologies.split(',').map((tech, i) => (
                <span 
                  key={i}
                  className="px-3 py-1 text-sm bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 rounded-full"
                >
                  {tech.trim()}
                </span>
              ))}
            </div>
          </div>
        </Link>
      ))}
    </div>
  )
}
