import { ImageResponse } from 'next/og'

export function GET(request: Request) {
  let url = new URL(request.url)
  let title = url.searchParams.get('title') || 'Adolfo Colavito'

  return new ImageResponse(
    (
      <div tw="flex flex-col w-full h-full items-center justify-center bg-black">
        <div tw="flex flex-col md:flex-row w-full py-12 px-4 md:items-center justify-between p-8">
          <h2 tw="flex flex-col text-5xl font-bold tracking-tight text-left text-white">
            {title}
          </h2>
          <p tw="text-2xl text-gray-400">Ingegnere Informatico</p>
        </div>
      </div>
    ),
    {
      width: 1200,
      height: 630,
    }
  )
}
