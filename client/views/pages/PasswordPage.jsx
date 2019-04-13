import React from 'react'
import { shape, number, string } from 'prop-types'
import Layout from '../components/Layout'
import Icon from '../components/Icon'
import FormErrorsTop from '../components/FormErrorsTop'
import FormErrorsField from '../components/FormErrorsField'

export default function PasswordPage({ gqlErrors, state, hash }) {
  return (
    <Layout
      hash={hash}
      page="PasswordPage"
      title="Change your password"
      description="Update your Sagefy account password. Log back into your account and get learning again today."
    >
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />

      <section>
        <h1>
          Change your password <Icon i="password" s="xxl" />
        </h1>

        <ol>
          {[
            { name: 'Enter your email', icon: 'email' },
            { name: 'Check your inbox', icon: 'inbox' },
            { name: 'Change your password', icon: 'password' },
          ].map(({ name, icon }, index) => (
            <li key={`PasswordPage-steps-${name}`}>
              {index === state ? (
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

        {state === 0 && (
          <form action="" method="POST">
            <input type="hidden" name="state" value="0" />
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
        )}

        {state === 1 && <p>Please check your email inbox.</p>}

        {state === 2 && (
          <form action="" method="POST">
            <input type="hidden" name="state" value="2" />
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
            </p>
            <FormErrorsField formErrors={gqlErrors} field="newPassword" />
            <p>
              <button type="submit">
                <Icon i="password" /> Update Password
              </button>
            </p>
          </form>
        )}
      </section>
    </Layout>
  )
}

PasswordPage.propTypes = {
  hash: string.isRequired,
  gqlErrors: shape({}),
  state: number,
}

PasswordPage.defaultProps = {
  gqlErrors: {},
  state: 0,
}
