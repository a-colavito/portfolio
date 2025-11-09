import { ImageResponse } from 'next/og'

export const size = {
  width: 32,
  height: 32,
}

export const contentType = 'image/png'

export default function Icon() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '0%',
          height: '0%',
          display: 'flex',
          background: 'transparent',
        }}
      />
    ),
    {
      ...size,
    }
  )
}
