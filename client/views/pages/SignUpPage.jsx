import React from 'react'
import { Link } from 'react-router-dom'
import { shape } from 'prop-types'
import Icon from '../components/Icon'

export default function SignUpPage({
  formErrors,
  prevValues: { name, email },
}) {
  return (
    <div className="SignUpPage">
      {Object.keys(formErrors).length > 0 && (
        <div className="FormErrors">
          <p>
            <mark>
              <Icon i="error" /> I couldn&apos;t do that...
            </mark>
          </p>
          {formErrors.all && (
            <ul>
              {formErrors.all.map(message => (
                <li>
                  <mark>{message}</mark>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

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
          By signing up, you agree to our
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
            {formErrors.name && (
              <ul>
                {formErrors.name.map(message => (
                  <li>
                    <mark>{message}</mark>
                  </li>
                ))}
              </ul>
            )}
          </p>
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
            {formErrors.email && (
              <ul>
                {formErrors.email.map(message => (
                  <li>
                    <mark>{message}</mark>
                  </li>
                ))}
              </ul>
            )}
          </p>
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
            {formErrors.password && (
              <ul>
                {formErrors.password.map(message => (
                  <li>
                    <mark>{message}</mark>
                  </li>
                ))}
              </ul>
            )}
          </p>
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
  formErrors: null,
  prevValues: null,
}
