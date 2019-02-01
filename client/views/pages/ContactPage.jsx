import React from 'react'
import { Link } from 'react-router-dom'
import Icon from '../components/Icon'

export default function ContactPage() {
  return (
    <div className="ContactPage">
      <section>
        <h1>
          Need help? <Icon i="contact" s="xxl" />
        </h1>
        <ul>
          <li>
            <strong>I have a problem with content.</strong>
            <br />
            <Icon i="talk" /> Discuss it in the site.
          </li>
          <li>
            <strong>I have an idea for content.</strong>
            <br />
            <Link to="/suggest">
              <Icon i="suggest" /> Suggest
            </Link>
            .
          </li>
          <li>
            <strong>I have an idea for the software.</strong>
            <br />
            <strong>I found a bug.</strong>
            <br />
            <a
              href="https://github.com/heiskr/sagefy/issues"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Icon i="github" /> Add to Github issues
            </a>
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
          </li>
        </ul>

        <p>
          <Link to="/">
            Go back <Icon i="home" /> home
          </Link>
        </p>
      </section>
    </div>
  )
}
