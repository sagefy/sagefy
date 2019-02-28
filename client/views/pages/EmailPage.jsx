import React from 'react'
import { shape, number } from 'prop-types'
import Icon from '../components/Icon'
import FormErrorsTop from '../components/FormErrorsTop'
import FormErrorsField from '../components/FormErrorsField'

export default function EmailPage({ formErrors, state }) {
  return (
    <div className="EmailPage">
      <FormErrorsTop formErrors={formErrors} />
      <FormErrorsField formErrors={formErrors} field="all" />

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
            <FormErrorsField formErrors={formErrors} field="email" />
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
              <label htmlFor="email">New Email</label>
              <input
                id="email"
                name="email"
                placeholder="example: unicorn@example.com"
                type="email"
                size="40"
                required
                autoFocus
              />
            </p>
            <FormErrorsField formErrors={formErrors} field="email" />
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
  formErrors: shape({}),
  prevValues: shape({}),
  state: number,
}

EmailPage.defaultProps = {
  formErrors: {},
  prevValues: {},
  state: 0,
}
