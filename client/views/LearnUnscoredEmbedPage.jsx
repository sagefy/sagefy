import React from 'react'
import { number, string, shape } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'

export default function LearnUnscoredEmbedPage({
  hash,
  progress,
  card: {
    entityId,
    name,
    data: { url },
  },
}) {
  return (
    <Layout
      hash={hash}
      page="LearnUnscoredEmbedPage"
      title="Learn"
      description="-"
      canonical={`/unscored-embed-cards/${to58(entityId)}`}
    >
      {progress && (
        <section>
          <progress value={progress} />
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

LearnUnscoredEmbedPage.propTypes = {
  hash: string.isRequired,
  progress: number,
  card: shape({
    name: string.isRequired,
    data: shape({
      url: string.isRequired,
    }).isRequired,
  }).isRequired,
}

LearnUnscoredEmbedPage.defaultProps = {
  progress: null,
}
