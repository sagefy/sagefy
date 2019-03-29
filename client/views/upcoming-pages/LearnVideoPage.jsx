import React from 'react'
import Icon from '../components/Icon'

export default function LearnVideoPage() {
  return (
    <div className="LearnVideoPage">
      <section>
        <progress value={0.7} />
      </section>

      <section>
        <iframe
          src="https://www.youtube.com/embed/qAojF80nwsM?autoplay=1&amp;modestbranding=1&amp;rel=0"
          width="600"
          height="400"
          allowFullScreen="true"
          title="Learn Video"
        />
      </section>

      <section>
        <form action="/learn-choice/1">
          <button type="submit">
            <Icon i="card" /> Next Card
          </button>
        </form>
      </section>
    </div>
  )
}
