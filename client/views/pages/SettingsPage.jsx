import React from 'react'
import { Link } from 'react-router-dom'
import { shape, string } from 'prop-types'
import Layout from '../components/Layout'
import Icon from '../components/Icon'
import FormErrorsTop from '../components/FormErrorsTop'
import FormErrorsField from '../components/FormErrorsField'

export default function SettingsPage({ hash, gqlErrors, body: { id, name } }) {
  return (
    <Layout hash={hash} page="SettingsPage" title="Settings" description="-">
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />

      <section>
        <h1>
          Update your settings <Icon i="settings" s="xxl" />
        </h1>
        <p>
          <Link to="/password">
            <Icon i="password" /> Change my password
          </Link>
          .
          <br />
          or{' '}
          <Link to="/email">
            <Icon i="email" /> Change my email
          </Link>
          .
        </p>
        <form action="" method="POST">
          <input type="hidden" name="id" value={id} />
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
          <FormErrorsField formErrors={gqlErrors} field="name" />
          {/* <p>
      <label for="email">Email</label>
      <input id="email" name="email" placeholder="ex: unicorn@example.com" type="email" size="40" value="doris@example.com">
    </p>
    <div>
      <label for="settings.email_frequency">Email Frequency</label>
      <ul class="ls-i" style="margin-top:0">
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
    </Layout>
  )
}

SettingsPage.propTypes = {
  hash: string.isRequired,
  gqlErrors: shape({}),
  body: shape({}),
}

SettingsPage.defaultProps = {
  gqlErrors: {},
  body: {},
}
