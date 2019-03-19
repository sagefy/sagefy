import React from 'react'
import Icon from '../components/Icon'

export default function LearnUnscoredEmbedPage() {
  return (
    <div className="LearnUnscoredEmbedPage">
      <section>
        <div className="meter">
          <div style={{ width: '95%' }} />
        </div>
      </section>

      <section>
        <iframe
          src="https://em.sagefy.org/examples/duration-and-rhythm"
          width="600"
          height="400"
          frameBorder="0"
          className="lift"
          title="Name of the embed card"
        />
      </section>

      <section>
        <form action="/choose-next">
          <button type="submit">
            <Icon i="card" /> Next Card
          </button>
        </form>
      </section>
    </div>
  )
}
