import React from 'react'
import { shape, number } from 'prop-types'
import Icon from '../components/Icon'
import FormErrorsTop from '../components/FormErrorsTop'
import FormErrorsField from '../components/FormErrorsField'

export default function PasswordPage({ formErrors, state }) {
  return (
    <div className="PasswordPage">
      <FormErrorsTop formErrors={formErrors} />
      <FormErrorsField formErrors={formErrors} field="all" />

      <section>
        <h1>
          Change your password <Icon i="password" s="xxl" />
        </h1>

        <ol>
          {[
            { name: 'Enter Email', icon: 'email' },
            { name: 'Check Inbox', icon: 'inbox' },
            { name: 'Change Password', icon: 'password' },
          ].map(({ name, icon }, index) => (
            <li>
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
            <FormErrorsField formErrors={formErrors} field="email" />
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
              <label htmlFor="password">Password</label>
              <input
                id="password"
                name="password"
                type="password"
                size="40"
                required
                autoFocus
                pattern=".{8,}"
              />
            </p>
            <FormErrorsField formErrors={formErrors} field="password" />
            <p>
              <button type="submit">
                <Icon i="password" /> Update Password
              </button>
            </p>
          </form>
        )}
      </section>
    </div>
  )
}

PasswordPage.propTypes = {
  formErrors: shape({}),
  prevValues: shape({}),
  state: number,
}

PasswordPage.defaultProps = {
  formErrors: {},
  prevValues: {},
  state: 0,
}
