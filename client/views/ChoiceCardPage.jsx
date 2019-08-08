import React from 'react'
import { shape, string } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import ReactMarkdown from 'react-markdown'
import Layout from './components/Layout'
import Icon from './components/Icon'
import Menu from './components/Menu'

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
        <Menu
          items={[
            {
              href: `/choice-cards/${to58(cardEntityId)}/talk`,
              icon: 'talk',
              name: 'Talk',
            },
            {
              href: `/choice-cards/${to58(cardEntityId)}/history`,
              icon: 'history',
              name: 'History',
            },
            {
              href: `/choice-cards/${to58(cardEntityId)}/edit`,
              icon: 'edit',
              name: 'Edit',
            },
          ]}
        />
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
