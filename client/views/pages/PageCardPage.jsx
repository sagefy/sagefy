import React from 'react'
import { Link } from 'react-router-dom'
import { shape, string } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import ReactMarkdown from 'react-markdown'
import Layout from '../components/Layout'
import Icon from '../components/Icon'

export default function PageCardPage({
  hash,
  card: {
    name: cardName,
    data: { body },
    subject: { name: subjectName, entityId: subjectEntityId },
  },
}) {
  return (
    <Layout
      hash={hash}
      page="PageCardPage"
      title={`Card: ${cardName}`}
      description="-"
    >
      <header>
        <div className="m-yc">
          <p>
            Page Card <Icon i="card" />
            <Icon i="page" />
          </p>
          <h1>{cardName}</h1>
        </div>
        <p>
          Belongs to subject{' '}
          <Link to={`/subjects/${to58(subjectEntityId)}`}>{subjectName}</Link>
          {/* TODO breadcrumbs? */}
        </p>
        <form method="GET" action="/next">
          <input type="hidden" name="goal" value={to58(subjectEntityId)} />
          <button type="submit">
            <Icon i="select" /> Let&apos;s learn now
          </button>
        </form>
        {/* TODO <small>
    <ul class="ls-i ta-r">
      <li><a href="/mocks/follows">👂🏿 Follow</a></li>
      <li><a href="/mocks/talk">💬 Talk</a></li>
      <li><a href="/mocks/history">🎢 History</a></li>
      <li><a href="/mocks/update-card">🌳 Edit</a></li>
    </ul>
  </small> */}
        {/* TODO stats */}
      </header>

      <section>
        <ReactMarkdown source={body} />
      </section>
    </Layout>
  )
}

PageCardPage.propTypes = {
  hash: string.isRequired,
  card: shape({
    name: string.isRequired,
    subject: shape({
      name: string.isRequired,
      entityId: string.isRequired,
    }).isRequired,
  }).isRequired,
}
