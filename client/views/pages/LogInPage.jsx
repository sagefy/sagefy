import React from 'react'
import { Link } from 'react-router-dom'
import { shape } from 'prop-types'
import Icon from '../components/Icon'
import FormErrorsTop from '../components/FormErrorsTop'
import FormErrorsField from '../components/FormErrorsField'

export default function LogInPage({ formErrors, prevValues: { name } }) {
  return (
    <div className="LogInPage">
      <FormErrorsTop formErrors={formErrors} />
      <FormErrorsField formErrors={formErrors} field="all" />

      <section>
        <h1>
          Log in to Sagefy <Icon i="logIn" s="xxl" />
        </h1>

        <p>
          Don&apos;t have an account?{' '}
          <Link to="/sign-up">
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
          <FormErrorsField formErrors={formErrors} field="name" />
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
          <FormErrorsField formErrors={formErrors} field="password" />
          <p>
            <button type="submit">
              <Icon i="logIn" /> Log In
            </button>
          </p>
        </form>
      </section>
    </div>
  )
}

LogInPage.propTypes = {
  formErrors: shape({}),
  prevValues: shape({}),
}

LogInPage.defaultProps = {
  formErrors: {},
  prevValues: {},
}
