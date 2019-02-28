import React from 'react'
import { Link } from 'react-router-dom'
import { shape } from 'prop-types'
import Icon from '../components/Icon'
import FormErrorsTop from '../components/FormErrorsTop'
import FormErrorsField from '../components/FormErrorsField'

export default function SettingsPage({ formErrors, prevValues: { name } }) {
  return (
    <div className="EmailPage">
      <FormErrorsTop formErrors={formErrors} />
      <FormErrorsField formErrors={formErrors} field="all" />

      <section>
        <h1>
          Update my settings <Icon i="settings" s="xxl" />
        </h1>
        <p>
          <Link to="/password">
            <Icon i="password" /> Change my password.
          </Link>{' '}
          or{' '}
          <Link to="/email">
            <Icon i="email" /> Change my email.
          </Link>
        </p>
        <form action="" method="POST">
          <p>
            <label htmlFor="name">Name</label>
            <input
              id="name"
              name="name"
              placeholder="ex: Unicorn"
              type="text"
              size="40"
              value={name}
              required
            />
          </p>
          <FormErrorsField formErrors={formErrors} field="name" />
          {/* <p>
      <label for="email">Email</label>
      <input id="email" name="email" placeholder="ex: unicorn@example.com" type="email" size="40" value="doris@example.com">
    </p>
    <div>
      <label for="settings.email_frequency">Email Frequency</label>
      <ul class="list-style-inline" style="margin-top:0">
        <li><label><input type="radio" value="immediate" name="settings.email_frequency" checked> Immediate</label></li>
        <li><label><input type="radio" value="daily" name="settings.email_frequency"> Daily</label></li>
        <li><label><input type="radio" value="weekly" name="settings.email_frequency"> Weekly</label></li>
        <li><label><input type="radio" value="never" name="settings.email_frequency"> Never</label></li>
      </ul>
    </div> */}
          <p>
            <button type="submit">
              <Icon i="settings" /> Update settings
            </button>
          </p>
        </form>
      </section>
    </div>
  )
}

SettingsPage.propTypes = {
  formErrors: shape({}),
  prevValues: shape({}),
}

SettingsPage.defaultProps = {
  formErrors: {},
  prevValues: {},
}
