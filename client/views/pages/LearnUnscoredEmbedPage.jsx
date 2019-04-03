import React from 'react'
import { number, string, shape } from 'prop-types'
import Icon from '../components/Icon'

export default function LearnUnscoredEmbedPage({
  progress,
  name,
  data: { url },
}) {
  return (
    <div className="LearnUnscoredEmbedPage">
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
    </div>
  )
}

LearnUnscoredEmbedPage.propTypes = {
  progress: number,
  name: string.isRequired,
  data: shape({
    url: string.isRequired,
  }).isRequired,
}

LearnUnscoredEmbedPage.defaultProps = {
  progress: null,
}
