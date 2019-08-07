import React from 'react'
import ReactMarkdown from 'react-markdown'
import { number, string, shape } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'

export default function LearnPageCardPage({
  hash,
  progress,
  card: {
    entityId,
    name,
    data: { body },
  },
}) {
  return (
    <Layout
      hash={hash}
      page="LearnPageCardPage"
      title="Learn"
      description="-"
      canonical={`/page-cards/${to58(entityId)}`}
    >
      {progress && (
        <section>
          <progress value={progress} />
        </section>
      )}

      <section>
        <h1>{name}</h1>
        <ReactMarkdown source={body} />
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

LearnPageCardPage.propTypes = {
  hash: string.isRequired,
  progress: number,
  card: shape({
    name: string.isRequired,
    data: shape({
      body: string.isRequired,
    }).isRequired,
  }).isRequired,
}

LearnPageCardPage.defaultProps = {
  progress: null,
}
