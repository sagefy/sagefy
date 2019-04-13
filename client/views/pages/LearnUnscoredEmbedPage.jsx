import React from 'react'
import { number, string, shape } from 'prop-types'
import Layout from '../components/Layout'
import Icon from '../components/Icon'

export default function LearnUnscoredEmbedPage({
  progress,
  card: {
    name,
    data: { url },
  },
}) {
  return (
    <Layout page="LearnUnscoredEmbedPage" title="Learn" description="-">
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
