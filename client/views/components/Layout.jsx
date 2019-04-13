import React from 'react'
import { string, node } from 'prop-types'

const hash = Date.now().toString(36)

export default function Layout({ title, description, children, page }) {
  if (process.env.NODE_ENV === 'test')
    return <div className={page}>{children}</div>
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{title} - Sagefy</title>
        <meta name="description" content={description} />
        <link rel="stylesheet" href={`/sagefy.min.css?${hash}`} />
      </head>
      <body>
        <div id="top" className={`page ${page}`} role="document">
          {children}
        </div>
      </body>
    </html>
  )
}

Layout.propTypes = {
  title: string.isRequired,
  description: string.isRequired,
  page: string.isRequired,
  children: node.isRequired,
}
