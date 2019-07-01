import React from 'react'
import { string, node, bool } from 'prop-types'

export default function Layout({
  page,
  title,
  description,
  hash,
  children,
  schema,
  typeOf,
}) {
  if (process.env.NODE_ENV === 'test') {
    return <div className={page}>{children}</div>
  }
  return (
    <html lang="en">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{title} - Sagefy</title>
        <meta name="description" content={description} />
        <meta name="twitter:card" content="summary" />
        <meta name="twitter:site" content="@sagefyorg" />
        <meta name="twitter:title" content={`${title} - Sagefy`} />
        <meta name="twitter:description" content={description} />
        <link rel="stylesheet" href={`/sagefy.min.css?${hash}`} />
      </head>
      <body vocab={schema && 'http://schema.org/'} typeof={typeOf}>
        <div id="top" className={page} role="document">
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
  hash: string.isRequired,
  schema: bool.isRequired,
  typeOf: string,
}

Layout.defaultProps = {
  typeOf: null,
}
