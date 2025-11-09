import { compile, run } from '@mdx-js/mdx'
import * as runtime from 'react/jsx-runtime'
import React from 'react'
import Image from 'next/image'

const components = {
  Image,
}

export async function CustomMDX({ source }: { source: string }) {
  const code = String(await compile(source, { outputFormat: 'function-body' }))
  const { default: MDXContent } = await run(code, { 
    ...runtime, 
    Fragment: React.Fragment 
  })
  
  return (
    <div className="prose prose-neutral dark:prose-invert">
      <MDXContent components={components} />
    </div>
  )
}
