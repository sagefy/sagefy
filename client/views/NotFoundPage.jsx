import React from 'react'
import { string } from 'prop-types'
import Layout from './components/Layout'
import Icon from './components/Icon'

export default function NotFoundPage({ hash }) {
  return (
    <Layout
      hash={hash}
      page="NotFoundPage"
      title="Not Found"
      description="Sagefy did not find that page."
    >
      <section>
        <h1>
          I couldn&apos;t find that page <Icon i="error" s="h1" />
        </h1>
        <p>
          <Icon i="error" /> 404 Not Found <Icon i="error" />{' '}
        </p>
        <p>
          <a href="/">
            Go back <Icon i="home" /> home
          </a>
        </p>
      </section>
    </Layout>
  )
}

NotFoundPage.propTypes = { hash: string.isRequired }
