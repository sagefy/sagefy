import React from 'react'
import { shape, string } from 'prop-types'
import Layout from './components/Layout'
import Icon from './components/Icon'
import FormErrorsTop from './components/FormErrorsTop'
import FormErrorsField from './components/FormErrorsField'
import Wizard from './components/Wizard'
import ExternalLink from './components/ExternalLink'

export default function EditPasswordPage({ gqlErrors, hash }) {
  return (
    <Layout
      hash={hash}
      page="EditPasswordPage"
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
          currentIndex={2}
        />

        <form action="" method="POST">
          <p>
            <label htmlFor="newPassword">Password</label>
            <input
              id="newPassword"
              name="newPassword"
              type="password"
              size="40"
              required
              autoFocus
              pattern=".{8,}"
            />
            <br />
            <small>
              Please{' '}
              <ExternalLink href="https://heiskr.com/use-a-password-manager/">
                use a password manager
              </ExternalLink>
              .
            </small>
          </p>
          <FormErrorsField formErrors={gqlErrors} field="newPassword" />
          <p>
            <button type="submit">
              <Icon i="password" /> Update Password
            </button>
          </p>
        </form>
      </section>
    </Layout>
  )
}

EditPasswordPage.propTypes = {
  hash: string.isRequired,
  gqlErrors: shape({}),
}

EditPasswordPage.defaultProps = {
  gqlErrors: {},
}
