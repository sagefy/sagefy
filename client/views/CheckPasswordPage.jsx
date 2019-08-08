import React from 'react'
import { string } from 'prop-types'
import Layout from './components/Layout'
import Icon from './components/Icon'
import Wizard from './components/Wizard'

export default function CheckPasswordPage({ hash }) {
  return (
    <Layout
      hash={hash}
      page="CheckPasswordPage"
      title="Change your password"
      description="Update your Sagefy account password. Log back into your account and get learning again today."
      canonical="/password"
    >
      <section>
        <h1>
          Change your password <Icon i="password" s="h1" />
        </h1>

        <Wizard
          steps={[
            { name: 'Enter your email', icon: 'email' },
            { name: 'Check your inbox', icon: 'inbox' },
            { name: 'Change your password', icon: 'password' },
          ]}
          currentIndex={1}
        />

        <p>Please check your email inbox.</p>
      </section>
    </Layout>
  )
}

CheckPasswordPage.propTypes = {
  hash: string.isRequired,
}
