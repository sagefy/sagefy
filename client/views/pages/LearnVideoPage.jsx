/* eslint-disable camelcase */

import React from 'react'
import { string, shape, number } from 'prop-types'
import Layout from '../components/Layout'
import Icon from '../components/Icon'

export default function LearnVideoPage({
  progress,
  card: {
    name,
    data: { video_id },
  },
}) {
  return (
    <Layout page="LearnVideoPage" title="Learn" description="-">
      {progress && (
        <section>
          <progress value={progress} />
        </section>
      )}

      <section>
        <iframe
          src={`https://www.youtube.com/embed/${video_id}?autoplay=1&amp;modestbranding=1&amp;rel=0`}
          width="600"
          height="400"
          allowFullScreen="true"
          title={name}
        />
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

LearnVideoPage.propTypes = {
  progress: number,
  card: shape({
    name: string.isRequired,
    data: shape({
      video_id: string.isRequired,
    }).isRequired,
  }).isRequired,
}

LearnVideoPage.defaultProps = {
  progress: null,
}
