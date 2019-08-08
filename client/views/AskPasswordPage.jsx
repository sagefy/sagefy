import React from 'react'
import { shape, string } from 'prop-types'
import Layout from './components/Layout'
import Icon from './components/Icon'
import FormErrorsTop from './components/FormErrorsTop'
import FormErrorsField from './components/FormErrorsField'
import Wizard from './components/Wizard'

export default function AskPasswordPage({ gqlErrors, hash }) {
  return (
    <Layout
      hash={hash}
      page="AskPasswordPage"
      title="Change your password"
      description="Update your Sagefy account password. Log back into your account and get learning again today."
      canonical="/password"
    >
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />

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
          currentIndex={0}
        />

        <form action="" method="POST">
          <p>
            <label htmlFor="email">Email</label>
            <input
              id="email"
              name="email"
              placeholder="example: unicorn@example.com"
              type="text"
              size="40"
              required
              autoFocus
            />
            <br />
            <small>We need your email to send the token.</small>
          </p>
          <FormErrorsField formErrors={gqlErrors} field="email" />
          <p>
            <button type="submit">
              <Icon i="password" /> Send Token
            </button>
          </p>
        </form>
      </section>
    </Layout>
  )
}

AskPasswordPage.propTypes = {
  hash: string.isRequired,
  gqlErrors: shape({}),
}

AskPasswordPage.defaultProps = {
  gqlErrors: {},
}
