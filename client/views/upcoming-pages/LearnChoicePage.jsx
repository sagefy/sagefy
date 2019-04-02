import React from 'react'
import Icon from '../components/Icon'
// TODO import ReactMarkdown from 'react-markdown'

export default function LearnChoicePage() {
  return (
    <div className="LearnChoicePage">
      <section>
        <progress value={0.7} />
      </section>

      <section>
        <div>
          <p>What is the difference between harmonic and inharmonic waves?</p>
        </div>
        <ul className="ls-n">
          <li>
            <input
              type="radio"
              name="choice"
              value="F0-61DPpSxqURHvryZy84Q"
              id="F0-61DPpSxqURHvryZy84Q"
              disabled
            />{' '}
            <label htmlFor="F0-61DPpSxqURHvryZy84Q" className="d-i">
              Both harmonics and inharmonics are integer multiples of the
              fundamental.
            </label>
          </li>
          <li>
            <input
              type="radio"
              name="choice"
              value="TT8B9zrBRkq5maek13ASJg"
              id="TT8B9zrBRkq5maek13ASJg"
              disabled
            />{' '}
            <label htmlFor="TT8B9zrBRkq5maek13ASJg" className="d-i">
              Inharmonics are integer multiples, harmonics are not.
            </label>
          </li>
          <li>
            <input
              type="radio"
              name="choice"
              value="R8eK8S_xQG2D6iJku1JS9Q"
              id="R8eK8S_xQG2D6iJku1JS9Q"
              disabled
              checked
            />{' '}
            <mark>
              <Icon i="check" /> Good job!
            </mark>{' '}
            <label htmlFor="R8eK8S_xQG2D6iJku1JS9Q" className="d-i">
              Harmonics are integer multiples, inharmonics are not.
            </label>
          </li>
          <li>
            <input
              type="radio"
              name="choice"
              value="lXQx9AQSQjKfSfIYy2OqWw"
              id="lXQx9AQSQjKfSfIYy2OqWw"
              disabled
            />{' '}
            <label htmlFor="lXQx9AQSQjKfSfIYy2OqWw" className="d-i">
              Neither harmonics nor inharmonics are integer multiples of the
              fundamental.
            </label>
          </li>
        </ul>
      </section>

      <section>
        <form action="/learn-page/1">
          <button type="submit">
            <Icon i="card" /> Next Card
          </button>
          {/* or, Check Answer */}
        </form>
      </section>
    </div>
  )
}
