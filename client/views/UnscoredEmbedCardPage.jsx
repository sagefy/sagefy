import React from 'react'
import { shape, string } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'

export default function UnscoredEmbedCardPage({
  hash,
  card: {
    entityId: cardEntityId,
    name: cardName,
    data: { url },
    subject: { name: subjectName, entityId: subjectEntityId },
  },
}) {
  return (
    <Layout
      hash={hash}
      page="UnscoredEmbedCardPage"
      title={`Card: ${cardName}`}
      description="-"
    >
      <header>
        <div className="my-c">
          <p>
            Embed Card <Icon i="card" />
            <Icon i="embed" />
          </p>
          <h1>{cardName}</h1>
        </div>
        <p>
          Belongs to subject{' '}
          <a href={`/subjects/${to58(subjectEntityId)}`}>{subjectName}</a>
          {/* TODO breadcrumbs? */}
        </p>
        <form method="GET" action="/next">
          <input type="hidden" name="goal" value={to58(subjectEntityId)} />
          <button type="submit">
            <Icon i="select" /> Let&apos;s learn now
          </button>
        </form>
        <small>
          <ul className="ls-i ta-r">
            {/* <li><a href="/mocks/follows">👂🏿 Follow</a></li> */}
            <li>
              <a href={`/unscored-embed-cards/${to58(cardEntityId)}/talk`}>
                <Icon i="talk" s="s" /> Talk
              </a>
            </li>
            <li>
              <a href={`/unscored-embed-cards/${to58(cardEntityId)}/history`}>
                <Icon i="history" s="s" /> History
              </a>
            </li>
            {/* <li><a href="/mocks/update-card">🌳 Edit</a></li> */}
          </ul>
        </small>
        {/* TODO stats */}
      </header>

      <section>
        <iframe src={url} width="600" height="400" title={cardName} />
      </section>
    </Layout>
  )
}

UnscoredEmbedCardPage.propTypes = {
  hash: string.isRequired,
  card: shape({
    name: string.isRequired,
    subject: shape({
      name: string.isRequired,
      entityId: string.isRequired,
    }).isRequired,
  }).isRequired,
}
