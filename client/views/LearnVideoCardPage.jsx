/* eslint-disable camelcase */

import React from 'react'
import { string, shape, number } from 'prop-types'
import { to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'

function getVideoUrl(site, video_id) {
  if (site === 'youtube')
    return `https://www.youtube.com/embed/${video_id}?autoplay=1&amp;modestbranding=1&amp;rel=0`
  if (site === 'vimeo') return `https://player.vimeo.com/video/${video_id}`
  return 'https://example.com'
}

export default function LearnVideoCardPage({
  hash,
  learned,
  card: {
    entityId,
    name,
    data: { site, video_id },
  },
  subject: { entityId: subjectId, name: subjectName },
}) {
  return (
    <Layout
      hash={hash}
      page="LearnVideoCardPage"
      title="Learn"
      canonical={`/video-cards/${to58(entityId)}`}
    >
      {learned && (
        <section>
          <progress value={learned} />
        </section>
      )}

      <section>
        <iframe
          src={getVideoUrl(site, video_id)}
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

LearnVideoCardPage.propTypes = {
  hash: string.isRequired,
  learned: number,
  card: shape({
    name: string.isRequired,
    data: shape({
      video_id: string.isRequired,
    }).isRequired,
  }).isRequired,
  subject: shape({
    name: string.isRequired,
    entityId: string.isRequired,
  }).isRequired,
}

LearnVideoCardPage.defaultProps = {
  learned: null,
}
