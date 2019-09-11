import React from 'react'
import { shape, string } from 'prop-types'
import Layout from './components/Layout'
import Icon from './components/Icon'
import FormErrorsTop from './components/FormErrorsTop'
import FormErrorsField from './components/FormErrorsField'
import ExternalLink from './components/ExternalLink'

export default function SignUpPage({
  hash,
  gqlErrors,
  body: { name, email },
  query: { redirect },
}) {
  return (
    <Layout
      hash={hash}
      page="SignUpPage"
      title="Join Sagefy"
      description="Get access to the best learning content with your Sagefy account. Continue where you left off on your learning journey."
    >
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />

      <section>
        <h1>
          Join Sagefy <Icon i="signUp" s="h1" />
        </h1>

        <p>
          Already have an account?{' '}
          <a href={redirect ? `/log-in?redirect=${redirect}` : '/log-in'}>
            <Icon i="logIn" /> Log In
          </a>
          .<br />
          By signing up, you agree to our{' '}
          <a href="/terms">
            <Icon i="terms" /> Terms of Service
          </a>
          .
        </p>

        <form action="" method="POST">
          <p>
            <label htmlFor="name">Name</label>
            <input
              id="name"
              name="name"
              placeholder="example: Unicorn"
              value={name}
              type="text"
              size="40"
              autoFocus
              required
            />
          </p>
          <FormErrorsField formErrors={gqlErrors} field="name" />
          <p>
            <label htmlFor="email">Email</label>
            <input
              id="email"
              name="email"
              placeholder="example: unicorn@example.com"
              value={email}
              type="email"
              size="40"
              required
            />
            <br />
            <small>
              We need your email to send notices and to reset your password.
            </small>
          </p>
          <FormErrorsField formErrors={gqlErrors} field="email" />
          <p>
            <label htmlFor="password">Password</label>
            <input
              id="password"
              name="password"
              type="password"
              size="40"
              required
              pattern=".{8,}"
            />
            <br />
            <small>
              Please{' '}
              <ExternalLink href="https://heiskr.com/useapasswordmanager/">
                use a password manager
              </ExternalLink>
              .
            </small>
          </p>
          <FormErrorsField formErrors={gqlErrors} field="password" />
          <p>
            <button type="submit">
              <Icon i="signUp" /> Sign Up
            </button>
          </p>
        </form>
      </section>
    </Layout>
  )
}

SignUpPage.propTypes = {
  hash: string.isRequired,
  gqlErrors: shape({}),
  body: shape({}),
  query: shape({}).isRequired,
}

SignUpPage.defaultProps = {
  gqlErrors: {},
  body: {},
}
