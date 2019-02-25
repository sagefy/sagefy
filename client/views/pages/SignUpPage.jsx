import React from 'react'
import { Link } from 'react-router-dom'
import { shape } from 'prop-types'
import Icon from '../components/Icon'
import FormErrorsTop from '../components/FormErrorsTop'
import FormErrorsField from '../components/FormErrorsField'

export default function SignUpPage({
  formErrors,
  prevValues: { name, email },
}) {
  return (
    <div className="SignUpPage">
      <FormErrorsTop formErrors={formErrors} />
      <FormErrorsField formErrors={formErrors} field="all" />

      <section>
        <h1>
          Join Sagefy <Icon i="signUp" s="xxl" />
        </h1>

        <p>
          Already have an account?{' '}
          <Link to="/log-in">
            <Icon i="logIn" /> Log In
          </Link>
          .<br />
          By signing up, you agree to our{' '}
          <Link to="/terms">
            <Icon i="terms" /> Terms of Service
          </Link>
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
          <FormErrorsField formErrors={formErrors} field="name" />
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
          <FormErrorsField formErrors={formErrors} field="email" />
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
              <Icon i="signUp" /> Sign Up
            </button>
          </p>
        </form>
      </section>
    </div>
  )
}

SignUpPage.propTypes = {
  formErrors: shape({}),
  prevValues: shape({}),
}

SignUpPage.defaultProps = {
  formErrors: {},
  prevValues: {},
}