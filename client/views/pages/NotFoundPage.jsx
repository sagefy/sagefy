import React from 'react'
import { Link } from 'react-router-dom'
import Layout from '../components/Layout'
import Icon from '../components/Icon'

export default function NotFoundPage() {
  return (
    <Layout
      page="NotFoundPage"
      title="Not Found"
      description="Sagefy did not find that page."
    >
      <section>
        <h1>
          I couldn&apos;t find that page <Icon i="error" s="xxl" />
        </h1>
        <p>
          <Icon i="error" /> 404 Not Found <Icon i="error" />{' '}
        </p>
        <p>
          <Link to="/">
            Go back <Icon i="home" /> home
          </Link>
        </p>
      </section>
    </Layout>
  )
}
