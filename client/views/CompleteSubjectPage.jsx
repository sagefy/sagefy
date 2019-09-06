import React from 'react'
import { string, shape } from 'prop-types'
import { to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import ExternalLink from './components/ExternalLink'

export default function CompleteSubjectPage({
  hash,
  role,
  subject: { name, entityId },
}) {
  return (
    <Layout
      hash={hash}
      page="CompleteSubjectPage"
      title={`Hooray! You just finished ${name}`}
      description="Congratulations!"
      canonical={`/subjects/${to58(entityId)}`}
    >
      <header className="my-c">
        <p>
          <em>
            Congratulations! <Icon i="cheer" /> You just finished&hellip;
          </em>
        </p>
        <h1>
          <q>{name}</q> <Icon i="subject" s="h1" />
        </h1>
      </header>
      <section className="ta-c">
        <Icon i="star" s="h1" />
        <Icon i="star" s="h1" />
        <Icon i="star" s="h1" />
        <Icon i="star" s="h1" />
        <Icon i="star" s="h1" />
        <p>Take a moment to appreciate your hard work!</p>
      </section>
      <section>
        <h2>
          What&apos;s next? <Icon i="search" s="h2" />
        </h2>
        <ul>
          <li>
            Share the subject on social media:
            <ul className="ls-n">
              <li>
                <ExternalLink
                  href={`https://twitter.com/intent/tweet?text=${encodeURIComponent(
                    `I just finished ${name} on Sagefy https://sagefy.org/subjects/${to58(
                      entityId
                    )}`
                  )}`}
                >
                  <Icon i="twitter" /> Twitter
                </ExternalLink>
              </li>
              <li>
                <ExternalLink
                  href={`https://www.facebook.com/sharer/sharer.php?u=https://sagefy.org/subjects/${to58(
                    entityId
                  )}`}
                >
                  <Icon i="facebook" /> Facebook
                </ExternalLink>
              </li>
              <li>
                <ExternalLink
                  href={`https://www.linkedin.com/sharing/share-offsite?url=https://sagefy.org/subjects/${to58(
                    entityId
                  )}`}
                >
                  <Icon i="linkedin" /> LinkedIn
                </ExternalLink>
              </li>
            </ul>
          </li>
          <li>
            <a href={`/subjects/${to58(entityId)}`}>
              Help contribute to the subject <Icon i="build" />
            </a>
          </li>
          {role === 'sg_anonymous' ? (
            <li>
              <a href="/subjects/search">
                Find your next subject <Icon i="search" />
              </a>
            </li>
          ) : (
            <li>
              <a href="/dashboard">
                Return back to your dashboard <Icon i="dashboard" />
              </a>
            </li>
          )}
        </ul>
      </section>
    </Layout>
  )
}

CompleteSubjectPage.propTypes = {
  hash: string.isRequired,
  role: string,
  subject: shape({}).isRequired,
}

CompleteSubjectPage.defaultProps = { role: 'sg_anonymous' }
