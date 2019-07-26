import React from 'react'
import { string } from 'prop-types'
import Layout from './components/Layout'
import Icon from './components/Icon'

export default function EmailPage({ hash }) {
  return (
    <Layout
      hash={hash}
      page="EmailPage"
      title="Change your email"
      description="Update your email address for your Sagefy account."
      canonical="/email"
    >
      <section>
        <h1>
          Change your email <Icon i="email" s="h1" />
        </h1>

        <ol>
          {[
            { name: 'Enter your current email', icon: 'email' },
            { name: 'Check your inbox', icon: 'inbox' },
            { name: 'Change your email', icon: 'email' },
          ].map(({ name, icon }, index) => (
            <li key={`EmailPage-steps-${name}`}>
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

EmailPage.propTypes = {
  hash: string.isRequired,
}
