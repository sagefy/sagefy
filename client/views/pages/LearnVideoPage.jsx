/* eslint-disable camelcase */

import React from 'react'
import { string, shape, number } from 'prop-types'
import Icon from '../components/Icon'

export default function LearnVideoPage({ progress, name, data: { video_id } }) {
  return (
    <div className="LearnVideoPage">
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
    </div>
  )
}

LearnVideoPage.propTypes = {
  progress: number,
  name: string.isRequired,
  data: shape({
    video_id: string.isRequired,
  }).isRequired,
}

LearnVideoPage.defaultProps = {
  progress: null,
}
