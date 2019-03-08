import React from 'react'
import { shape, number } from 'prop-types'
import Icon from '../components/Icon'
import FormErrorsTop from '../components/FormErrorsTop'
import FormErrorsField from '../components/FormErrorsField'

export default function EmailPage({ gqlErrors, state }) {
  return (
    <div className="EmailPage">
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />

      <section>
        <h1>
          Change your email <Icon i="email" s="xxl" />
        </h1>

        <ol>
          {[
            { name: 'Enter Current Email', icon: 'email' },
            { name: 'Check Inbox', icon: 'inbox' },
            { name: 'Change Email', icon: 'email' },
          ].map(({ name, icon }, index) => (
            <li key={`EmailPage-steps-${name}`}>
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
              <label htmlFor="email">Current Email</label>
              <input
                id="email"
                name="email"
                placeholder="example: unicorn@example.com"
                type="email"
                size="40"
                required
                autoFocus
              />
              <br />
              <small>We need your current email to send the token.</small>
            </p>
            <FormErrorsField formErrors={gqlErrors} field="email" />
            <p>
              <button type="submit">
                <Icon i="email" /> Send Token
              </button>
            </p>
          </form>
        )}

        {state === 1 && <p>Please check your email inbox.</p>}

        {state === 2 && (
          <form action="" method="POST">
            <input type="hidden" name="state" value="2" />
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
        )}
      </section>
    </div>
  )
}

EmailPage.propTypes = {
  gqlErrors: shape({}),
  state: number,
}

EmailPage.defaultProps = {
  gqlErrors: {},
  state: 0,
}
