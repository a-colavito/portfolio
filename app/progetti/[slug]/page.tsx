import { notFound } from 'next/navigation'
import { CustomMDX } from 'app/components/mdx'
import { getProjects, getProject } from '../utils'
import { baseUrl } from 'app/sitemap'

export async function generateStaticParams() {
  let projects = getProjects()

  return projects.map((project) => ({
    slug: project.slug,
  }))
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  let project = getProject(slug)
  if (!project) {
    return
  }

  let {
    title,
    publishedAt: publishedTime,
    summary: description,
    image,
  } = project.metadata
  let ogImage = image
    ? image
    : `${baseUrl}/og?title=${encodeURIComponent(title)}`

  return {
    title,
    description,
    openGraph: {
      title,
      description,
      type: 'article',
      publishedTime,
      url: `${baseUrl}/progetti/${project.slug}`,
      images: [
        {
          url: ogImage,
        },
      ],
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
      images: [ogImage],
    },
  }
}

export default async function Project({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  let project = getProject(slug)

  if (!project) {
    notFound()
  }

  return (
    <section>
      <script
        type="application/ld+json"
        suppressHydrationWarning
        dangerouslySetInnerHTML={{
          __html: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'SoftwareSourceCode',
            headline: project.metadata.title,
            datePublished: project.metadata.publishedAt,
            description: project.metadata.summary,
            url: `${baseUrl}/progetti/${project.slug}`,
            author: {
              '@type': 'Person',
              name: 'Adolfo Colavito',
            },
          }),
        }}
      />
      <h1 className="title font-semibold text-2xl tracking-tighter">
        {project.metadata.title}
      </h1>
      <div className="flex justify-between items-center mt-2 mb-8 text-sm">
        <p className="text-sm text-neutral-600 dark:text-neutral-400">
          {new Date(project.metadata.publishedAt).toLocaleDateString('it-IT', {
            year: 'numeric',
            month: 'long',
          })}
        </p>
        {project.metadata.github && (
          <a
            href={project.metadata.github}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 underline"
          >
            GitHub →
          </a>
        )}
      </div>
      <div className="flex flex-wrap gap-2 mb-8">
        {project.metadata.technologies.split(',').map((tech, i) => (
          <span
            key={i}
            className="px-3 py-1 text-sm bg-neutral-100 dark:bg-neutral-800 text-neutral-700 dark:text-neutral-300 rounded-full"
          >
            {tech.trim()}
          </span>
        ))}
      </div>
      <article className="prose">
        <CustomMDX source={project.content} />
      </article>
    </section>
  )
}
