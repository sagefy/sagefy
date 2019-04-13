/* eslint-disable jsx-a11y/anchor-is-valid, no-script-url */

import React from 'react'
import { Link } from 'react-router-dom'
import Layout from '../components/Layout'
import Icon from '../components/Icon'

export default function ServerErrorPage() {
  return (
    <Layout page="ServerErrorPage" title="Server error" description="-">
      <section>
        <h1>
          I couldn&apos;t make that happen <Icon i="error" s="xxl" />
        </h1>
        <p>
          <Icon i="error" /> 500 Server Error <Icon i="error" />{' '}
        </p>
        <p>
          <Link to="/">
            Go back <Icon i="home" /> home
          </Link>{' '}
          &bull; You can also{' '}
          <a href="javascript:history.back()">
            <Icon i="left" /> go back
          </a>{' '}
          and retry.
        </p>
      </section>
    </Layout>
  )
}
