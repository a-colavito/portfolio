import path from 'path'
import { getMDXData, ProjectMetadata, MDXData } from '@/lib/mdx'

export function getProjects(): MDXData<ProjectMetadata>[] {
  return getMDXData<ProjectMetadata>(path.join(process.cwd(), 'app', 'progetti', 'projects'))
}

export function getProject(slug: string): MDXData<ProjectMetadata> | undefined {
  const projects = getProjects()
  return projects.find((project) => project.slug === slug)
}
