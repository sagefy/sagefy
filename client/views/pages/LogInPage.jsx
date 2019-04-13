import React from 'react'
import { Link } from 'react-router-dom'
import { shape, string } from 'prop-types'
import Layout from '../components/Layout'
import Icon from '../components/Icon'
import FormErrorsTop from '../components/FormErrorsTop'
import FormErrorsField from '../components/FormErrorsField'

export default function LogInPage({
  hash,
  gqlErrors,
  body: { name },
  query: { redirect },
}) {
  return (
    <Layout
      hash={hash}
      page="LogInPage"
      title="Log In"
      description="Log in to Sagefy. Continue learning your subjects. And help us make new content to grow Sagefy."
    >
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />

      <section>
        <h1>
          Log in to Sagefy <Icon i="logIn" s="xxl" />
        </h1>

        <p>
          Don&apos;t have an account?{' '}
          <Link to={redirect ? `/sign-up?redirect=${redirect}` : '/sign-up'}>
            <Icon i="signUp" /> Sign Up
          </Link>
          .<br />
          Forgot your password?{' '}
          <Link to="/password">
            <Icon i="password" /> Reset
          </Link>
          .
        </p>

        <form action="" method="POST">
          <p>
            <label htmlFor="name">Name or Email</label>
            <input
              id="name"
              name="name"
              placeholder="example: Unicorn"
              type="text"
              size="40"
              autoFocus
              value={name}
            />
          </p>
          <FormErrorsField formErrors={gqlErrors} field="name" />
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
          </p>
          <FormErrorsField formErrors={gqlErrors} field="password" />
          <p>
            <button type="submit">
              <Icon i="logIn" /> Log In
            </button>
          </p>
        </form>
      </section>
    </Layout>
  )
}

LogInPage.propTypes = {
  hash: string.isRequired,
  gqlErrors: shape({}),
  body: shape({}),
  query: shape({}).isRequired,
}

LogInPage.defaultProps = {
  gqlErrors: {},
  body: {},
}
