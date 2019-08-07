import React from 'react'
import { shape, string } from 'prop-types'
import Layout from './components/Layout'
import Icon from './components/Icon'
import FormErrorsTop from './components/FormErrorsTop'
import FormErrorsField from './components/FormErrorsField'

export default function EditEmailPage({ gqlErrors, hash }) {
  return (
    <Layout
      hash={hash}
      page="EditEmailPage"
      title="Change your email"
      description="Update your email address for your Sagefy account."
      canonical="/email"
    >
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />

      <section>
        <h1>
          Change your email <Icon i="email" s="h1" />
        </h1>
        <ol>
          {[
            { name: 'Enter your current email', icon: 'email' },
            { name: 'Check your inbox', icon: 'inbox' },
            { name: 'Change your email', icon: 'email' },
          ].map(({ name, icon }, index) => (
            <li key={`EmailPage-steps-${name}`}>
              {index === 2 ? (
                <strong>
                  {name} <Icon i={icon} />
                </strong>
              ) : (
                <span>
                  {name} <Icon i={icon} />
                </span>
              )}
            </li>
          ))}
        </ol>

        <form action="" method="POST">
          <p>
            <label htmlFor="newEmail">New Email</label>
            <input
              id="newEmail"
              name="newEmail"
              placeholder="example: unicorn@example.com"
              type="email"
              size="40"
              required
              autoFocus
            />
          </p>
          <FormErrorsField formErrors={gqlErrors} field="newEmail" />
          <p>
            <button type="submit">
              <Icon i="email" /> Update Email
            </button>
          </p>
        </form>
      </section>
    </Layout>
  )
}

EditEmailPage.propTypes = {
  hash: string.isRequired,
  gqlErrors: shape({}),
}

EditEmailPage.defaultProps = {
  gqlErrors: {},
}
