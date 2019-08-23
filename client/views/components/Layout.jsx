import React from 'react'
import { string, node } from 'prop-types'

const ROOT =
  process.env.NODE_ENV === 'production'
    ? 'https://sagefy.org'
    : 'http://localhost'

export default function Layout({
  page,
  title,
  description,
  image,
  hash,
  children,
  canonical,
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
        {description && <meta name="description" content={description} />}
        {canonical && <link rel="canonical" href={`${ROOT}${canonical}`} />}
        <meta name="twitter:card" content="summary" />
        <meta name="twitter:site" content="@sagefyorg" />
        <meta name="twitter:title" content={`${title} - Sagefy`} />
        {description && (
          <meta name="twitter:description" content={description} />
        )}
        {image && <meta name="twitter:image" content={image} />}
        <meta property="og:title" content={`${title} - Sagefy`} />
        {description && (
          <meta property="og:description" content={description} />
        )}
        <meta property="og:type" content="website" />
        {canonical && (
          <meta property="og:url" content={`${ROOT}${canonical}`} />
        )}
        {image && <meta property="og:image" content={image} />}
        <meta property="og:site_name" content="Sagefy" />
        <link rel="stylesheet" href={`/sagefy.min.css?${hash}`} />
      </head>
      <body>
        <div id="top" className={page} role="document">
          {children}
        </div>
      </body>
    </html>
  )
}

Layout.propTypes = {
  title: string.isRequired,
  description: string,
  page: string.isRequired,
  children: node.isRequired,
  hash: string.isRequired,
  image: string,
  canonical: string,
}

Layout.defaultProps = {
  description: null,
  image: null,
  canonical: null,
}
