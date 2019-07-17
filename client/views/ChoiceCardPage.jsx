import React from 'react'
import { shape, string } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import ReactMarkdown from 'react-markdown'
import Layout from './components/Layout'
import Icon from './components/Icon'

export default function ChoiceCardPage({
  hash,
  card: {
    entityId: cardEntityId,
    name: cardName,
    data: { body, options },
    subject: { name: subjectName, entityId: subjectEntityId },
  },
}) {
  return (
    <Layout
      hash={hash}
      page="ChoiceCardPage"
      title={`Card: ${cardName}`}
      description="-"
    >
      <header>
        <div className="my-c">
          <p>
            Choice Card <Icon i="card" />
            <Icon i="choice" />
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
        <small>
          <ul className="ls-i ta-r">
            {/* <li><a href="/mocks/follows">👂🏿 Follow</a></li> */}
            <li>
              <a href={`/choice-cards/${to58(cardEntityId)}/talk`}>
                <Icon i="talk" s="s" /> Talk
              </a>
            </li>
            <li>
              <a href={`/choice-cards/${to58(cardEntityId)}/history`}>
                <Icon i="history" s="s" /> History
              </a>
            </li>
            {/* <li><a href="/mocks/update-card">🌳 Edit</a></li> */}
          </ul>
        </small>
        {/* TODO stats */}
      </header>

      <section>
        <div alt={cardName}>
          <ReactMarkdown source={body} />
        </div>
        <ul>
          {Object.entries(options).map(
            ([key, { value, correct, feedback }]) => (
              <li key={key}>
                {value}
                <br />
                <mark className={correct ? 'good' : ''}>
                  {correct ? <Icon i="check" /> : <Icon i="error" />} {feedback}
                </mark>
              </li>
            )
          )}
        </ul>
      </section>
    </Layout>
  )
}

ChoiceCardPage.propTypes = {
  hash: string.isRequired,
  card: shape({
    name: string.isRequired,
    subject: shape({
      name: string.isRequired,
      entityId: string.isRequired,
    }).isRequired,
  }).isRequired,
}
