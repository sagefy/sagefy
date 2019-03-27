import React from 'react'
import Icon from './Icon'

export default function CardSubjectInfo() {
  return (
    <section className="CardSubjectInfo">
      <details>
        <summary>
          <span>
            What are cards &amp; subjects? <Icon i="card" />
            <Icon i="subject" />
          </span>
        </summary>
        <ul>
          <li>
            <p>
              A <strong>card</strong> <Icon i="card" /> is a single learning
              activity.
            </p>
            <blockquote>
              <p>Examples: a 3-minute video or a multiple choice question.</p>
            </blockquote>
          </li>
          <li>
            <p>
              A <strong>subject</strong> <Icon i="subject" /> is a collection of
              cards and other subjects.
            </p>
            <blockquote>
              <p>
                Like a course, but at any scale. Such as “Measures of Central
                Tendency”, “Intro to Statistics”, or even a complete statistics
                program.
              </p>
            </blockquote>
          </li>
        </ul>
      </details>
    </section>
  )
}
