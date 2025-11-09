import fs from 'fs'
import path from 'path'

export type BlogMetadata = {
  title: string
  publishedAt: string
  summary: string
  image?: string
}

export type ProjectMetadata = {
  title: string
  publishedAt: string
  summary: string
  technologies: string
  github?: string
  demo?: string
  image?: string
}

export type MDXData<T> = {
  metadata: T
  slug: string
  content: string
}

function parseFrontmatter(fileContent: string) {
  const frontmatterRegex = /---\s*([\s\S]*?)\s*---/
  const match = frontmatterRegex.exec(fileContent)
  if (!match) {
    throw new Error('Invalid frontmatter')
  }
  
  const frontMatterBlock = match[1]
  const content = fileContent.replace(frontmatterRegex, '').trim()
  const frontMatterLines = frontMatterBlock.trim().split('\n')
  const metadata: Record<string, string> = {}

  frontMatterLines.forEach((line) => {
    const [key, ...valueArr] = line.split(': ')
    let value = valueArr.join(': ').trim()
    value = value.replace(/^['"](.*)['"]$/, '$1') // Remove quotes
    metadata[key.trim()] = value
  })

  return { metadata, content }
}

function getMDXFiles(dir: string): string[] {
  return fs.readdirSync(dir).filter((file) => path.extname(file) === '.mdx')
}

function readMDXFile<T>(filePath: string): { metadata: T; content: string } {
  const rawContent = fs.readFileSync(filePath, 'utf-8')
  const { metadata, content } = parseFrontmatter(rawContent)
  return { metadata: metadata as T, content }
}

export function getMDXData<T>(dir: string): MDXData<T>[] {
  const mdxFiles = getMDXFiles(dir)
  return mdxFiles.map((file) => {
    const { metadata, content } = readMDXFile<T>(path.join(dir, file))
    const slug = path.basename(file, path.extname(file))

    return {
      metadata,
      slug,
      content,
    }
  })
}
