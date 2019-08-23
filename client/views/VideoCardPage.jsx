/* eslint-disable camelcase */
import React from 'react'
import { shape, string } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import Menu from './components/Menu'
import getMenuItems from '../util/get-menu-items'

function getVideoUrl(site, video_id) {
  if (site === 'youtube')
    return `https://www.youtube.com/embed/${video_id}?autoplay=1&amp;modestbranding=1&amp;rel=0`
  if (site === 'vimeo') return `https://player.vimeo.com/video/${video_id}`
  return 'https://example.com'
}

export default function VideoCardPage({
  hash,
  card: {
    entityId: cardEntityId,
    name: cardName,
    data: { site, video_id },
    subject: { name: subjectName, entityId: subjectEntityId },
  },
}) {
  return (
    <Layout
      hash={hash}
      page="VideoCardPage"
      title={`Card: ${cardName}`}
      canonical={`/video-cards/${to58(cardEntityId)}`}
    >
      <header>
        <div className="my-c">
          <p>
            Video Card <Icon i="card" />
            <Icon i="video" />
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

        <Menu items={getMenuItems('video-cards', to58(cardEntityId))} />
        {/* TODO stats */}
      </header>

      <section>
        <iframe
          src={getVideoUrl(site, video_id)}
          width="600"
          height="400"
          allowFullScreen="true"
          title={cardName}
        />
      </section>
    </Layout>
  )
}

VideoCardPage.propTypes = {
  hash: string.isRequired,
  card: shape({
    name: string.isRequired,
    subject: shape({
      name: string.isRequired,
      entityId: string.isRequired,
    }).isRequired,
  }).isRequired,
}
