import React from 'react'
import { string } from 'prop-types'
import Layout from './components/Layout'
import Icon from './components/Icon'
import Wizard from './components/Wizard'

export default function CheckEmailPage({ hash }) {
  return (
    <Layout
      hash={hash}
      page="CheckEmailPage"
      title="Change your email"
      description="Update your email address for your Sagefy account."
      canonical="/email"
    >
      <section>
        <h1>
          Change your email <Icon i="email" s="h1" />
        </h1>

        <Wizard
          steps={[
            { name: 'Enter your current email', icon: 'email' },
            { name: 'Check your inbox', icon: 'inbox' },
            { name: 'Change your email', icon: 'email' },
          ]}
          currentIndex={1}
        />

        <p>Please check your email inbox.</p>
      </section>
    </Layout>
  )
}

CheckEmailPage.propTypes = {
  hash: string.isRequired,
}
