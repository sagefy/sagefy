/* eslint-disable jsx-a11y/anchor-is-valid, no-script-url */

import React from 'react'
import { string } from 'prop-types'
import Layout from './components/Layout'
import Icon from './components/Icon'

export default function ServerErrorPage({ hash }) {
  return (
    <Layout hash={hash} page="ServerErrorPage" title="Server error">
      <section>
        <h1>
          I couldn&apos;t make that happen <Icon i="error" s="h1" />
        </h1>
        <p>
          <Icon i="error" /> 500 Server Error <Icon i="error" />{' '}
        </p>
        <p>
          <a href="/">
            Go back <Icon i="home" /> home
          </a>{' '}
          &bull; You can also <Icon i="left" /> go back and retry.
        </p>
      </section>
    </Layout>
  )
}

ServerErrorPage.propTypes = {
  hash: string.isRequired,
}
