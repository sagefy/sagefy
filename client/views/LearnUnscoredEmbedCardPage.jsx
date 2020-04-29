import React from 'react'
import { number, string, shape } from 'prop-types'
import { to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'

export default function LearnUnscoredEmbedCardPage({
  hash,
  learned,
  card: {
    entityId,
    name,
    data: { url },
  },
  subject: { entityId: subjectId, name: subjectName },
}) {
  return (
    <Layout
      hash={hash}
      page="LearnUnscoredEmbedCardPage"
      title="Learn"
      canonical={`/unscored-embed-cards/${to58(entityId)}`}
    >
      {learned && (
        <section>
          <progress value={learned} />
        </section>
      )}

      <section>
        <iframe src={url} width="600" height="400" title={name} />
      </section>

      <section>
        <form action="/next">
          <button type="submit">
            <Icon i="card" /> Next Card
          </button>
        </form>
      </section>
    </Layout>
  )
}

LearnUnscoredEmbedCardPage.propTypes = {
  hash: string.isRequired,
  learned: number,
  card: shape({
    name: string.isRequired,
    data: shape({
      url: string.isRequired,
    }).isRequired,
  }).isRequired,
  subject: shape({
    name: string.isRequired,
    entityId: string.isRequired,
  }).isRequired,
}

LearnUnscoredEmbedCardPage.defaultProps = {
  learned: null,
}
