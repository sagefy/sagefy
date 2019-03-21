import React from 'react'
import Icon from '../components/Icon'
import Meter from '../components/Meter'

export default function LearnVideoPage() {
  return (
    <div className="LearnVideoPage">
      <section>
        <Meter width={0.7} />
      </section>

      <section>
        <iframe
          className="video lift"
          src="https://www.youtube.com/embed/qAojF80nwsM?autoplay=1&amp;modestbranding=1&amp;rel=0"
          width="600"
          height="400"
          allowFullScreen="true"
          frameBorder="0"
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
