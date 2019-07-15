import React from 'react'
import { string } from 'prop-types'
import Layout from './components/Layout'
import Icon from './components/Icon'
import ExternalLink from './components/ExternalLink'

export default function ContactPage({ hash }) {
  return (
    <Layout
      hash={hash}
      page="ContactPage"
      title="Contact"
      description="Need help? Contact Sagefy support."
    >
      <section>
        <h1>
          Need help? <Icon i="contact" s="h1" />
        </h1>
        <ul>
          <li>
            <strong>I have a problem with content.</strong>
            <br />
            <a href="/search">
              <Icon i="talk" /> Discuss it in the site
            </a>
            .
          </li>
          <li>
            <strong>I have an idea for content.</strong>
            <br />
            <a href="/create-subject">
              <Icon i="subject" /> Create a new subject
            </a>
            .
          </li>
          <li>
            <strong>I have an idea for the software.</strong>
            <br />
            <strong>I found a bug.</strong>
            <br />
            <ExternalLink href="https://github.com/heiskr/sagefy/issues">
              <Icon i="github" /> Add to Github issues
            </ExternalLink>
            .
          </li>
          <li>
            <strong>I found a security issue.</strong>
            <br />
            <strong>I need help with my account.</strong>
            <br />
            <strong>My copyright has been violated.</strong>
            <br />
            <strong>I&apos;m a media person.</strong>
            <br />
            <a href="mailto:support@sagefy.org">
              <Icon i="contact" /> Send us an email
            </a>
            .
          </li>
        </ul>
        <p>
          <a href="/">
            Go back <Icon i="home" /> home
          </a>
        </p>
      </section>
    </Layout>
  )
}

ContactPage.propTypes = { hash: string.isRequired }
