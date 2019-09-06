import React from 'react'
import ReactMarkdown from 'react-markdown'
import { number, string, shape } from 'prop-types'
import { to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import TempHelp from './components/TempHelp'

export default function LearnPageCardPage({
  hash,
  learned,
  card: {
    entityId,
    name,
    data: { body },
  },
  subject: { entityId: subjectId, name: subjectName },
}) {
  return (
    <Layout
      hash={hash}
      page="LearnPageCardPage"
      title="Learn"
      canonical={`/page-cards/${to58(entityId)}`}
    >
      {learned && (
        <section>
          <progress value={learned} />
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

      <TempHelp name={subjectName} subjectId={subjectId} cardId={entityId} />
    </Layout>
  )
}

LearnPageCardPage.propTypes = {
  hash: string.isRequired,
  learned: number,
  card: shape({
    name: string.isRequired,
    data: shape({
      body: string.isRequired,
    }).isRequired,
  }).isRequired,
  subject: shape({
    name: string.isRequired,
    entityId: string.isRequired,
  }).isRequired,
}

LearnPageCardPage.defaultProps = {
  learned: null,
}
