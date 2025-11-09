import { BlogPosts } from 'app/components/posts'

export const metadata = {
  title: 'Blog',
  description: 'Articoli su web development, tecnologia e programmazione.',
}

export default function Page() {
  return (
    <section>
      <h1 className="font-semibold text-xl sm:text-2xl mb-6 sm:mb-8 tracking-tighter">Blog</h1>
      <BlogPosts />
    </section>
  )
}
