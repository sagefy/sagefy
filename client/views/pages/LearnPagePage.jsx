import React from 'react'
import ReactMarkdown from 'react-markdown'
import { number, string, shape } from 'prop-types'
import Icon from '../components/Icon'

export default function LearnPagePage({ progress, name, data: { body } }) {
  return (
    <div className="LearnPagePage">
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
    </div>
  )
}

LearnPagePage.propTypes = {
  progress: number,
  name: string.isRequired,
  data: shape({
    body: string.isRequired,
  }).isRequired,
}

LearnPagePage.defaultProps = {
  progress: null,
}
