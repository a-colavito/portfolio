import { remark } from 'remark'
import html from 'remark-html'

export async function CustomMDX({ source }: { source: string }) {
  const result = await remark()
    .use(html, { sanitize: false })
    .process(source)
  
  const contentHtml = result.toString()

  return (
    <div 
      className="prose prose-neutral dark:prose-invert"
      dangerouslySetInnerHTML={{ __html: contentHtml }}
    />
  )
}
