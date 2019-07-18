import React from 'react'
import { string } from 'prop-types'
import Layout from './components/Layout'
import Icon from './components/Icon'

export default function PasswordPage({ hash }) {
  return (
    <Layout
      hash={hash}
      page="PasswordPage"
      title="Change your password"
      description="Update your Sagefy account password. Log back into your account and get learning again today."
    >
      <section>
        <h1>
          Change your password <Icon i="password" s="h1" />
        </h1>

        <ol>
          {[
            { name: 'Enter your email', icon: 'email' },
            { name: 'Check your inbox', icon: 'inbox' },
            { name: 'Change your password', icon: 'password' },
          ].map(({ name, icon }, index) => (
            <li key={`PasswordPage-steps-${name}`}>
              {index === 1 ? (
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

        <p>Please check your email inbox.</p>
      </section>
    </Layout>
  )
}

PasswordPage.propTypes = {
  hash: string.isRequired,
}
