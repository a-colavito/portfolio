import Link from 'next/link'
import { formatDate, getBlogPosts } from 'app/blog/utils'

export function BlogPosts({ limit }: { limit?: number }) {
  let allBlogs = getBlogPosts()

  return (
    <div>
      {allBlogs
        .sort((a, b) => {
          if (
            new Date(a.metadata.publishedAt) > new Date(b.metadata.publishedAt)
          ) {
            return -1
          }
          return 1
        })
        .slice(0, limit)
        .map((post) => (
          <Link
            key={post.slug}
            className="flex flex-col space-y-1 mb-4 sm:mb-5"
            href={`/blog/${post.slug}`}
          >
            <div className="w-full flex flex-col sm:flex-row space-x-0 sm:space-x-2 space-y-0.5 sm:space-y-0">
              <p className="text-neutral-600 dark:text-neutral-400 text-xs sm:text-sm sm:w-[100px] tabular-nums flex-shrink-0">
                {formatDate(post.metadata.publishedAt, false)}
              </p>
              <p className="text-neutral-900 dark:text-neutral-100 tracking-tight text-sm sm:text-base font-medium">
                {post.metadata.title}
              </p>
            </div>
          </Link>
        ))}
    </div>
  )
}
