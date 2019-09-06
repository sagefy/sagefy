/* eslint-disable camelcase */
import React from 'react'
import ReactMarkdown from 'react-markdown'
import { string, number, shape, objectOf, bool } from 'prop-types'
import { shuffle } from 'shuffle-seed'
import { to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import TempHelp from './components/TempHelp'

export default function LearnChoiceCardPage({
  hash,
  learned,
  card: {
    entityId,
    name,
    data: { body, max_options_to_show, options },
  },
  subject: { entityId: subjectId, name: subjectName },
  body: {
    choice,
    seed = process.env.NODE_ENV === 'test' ? '_' : Date.now().toString(36),
  } = {},
}) {
  const xoptions = shuffle(Object.entries(options), seed).slice(
    0,
    max_options_to_show
  )
  return (
    <Layout
      hash={hash}
      page="LearnChoiceCardPage"
      title="Learn"
      canonical={`/choice-cards/${to58(entityId)}`}
    >
      {learned && (
        <section>
          <progress value={learned} />
        </section>
      )}

      <form action={choice ? '/next' : ''} method={choice ? 'GET' : 'POST'}>
        <section>
          <div alt={name}>
            <ReactMarkdown source={body} />
          </div>
          <ul className="ls-n">
            {xoptions.map(([key, { value, correct, feedback }]) => (
              <li key={key}>
                <input
                  type="radio"
                  name="choice"
                  value={key}
                  id={key}
                  disabled={choice}
                  checked={choice === key}
                />{' '}
                <label htmlFor={key} className="d-i">
                  {value}
                  {choice === key && <br />}
                  {choice === key && (
                    <mark className={correct ? 'good' : ''}>
                      {correct ? <Icon i="check" /> : <Icon i="error" />}{' '}
                      {feedback}
                    </mark>
                  )}
                </label>
              </li>
            ))}
            <input type="hidden" name="seed" value={seed} />
          </ul>
        </section>

        <section>
          {choice ? (
            <button type="submit">
              <Icon i="card" /> Next Card
            </button>
          ) : (
            <button type="submit">
              <Icon i="check" /> Check Answer
            </button>
          )}
        </section>
      </form>

      <TempHelp name={subjectName} subjectId={subjectId} cardId={entityId} />
    </Layout>
  )
}

LearnChoiceCardPage.propTypes = {
  hash: string.isRequired,
  learned: number,
  card: shape({
    name: string.isRequired,
    data: shape({
      body: string.isRequired,
      max_options_to_show: number.isRequired,
      options: objectOf(
        shape({
          value: string.isRequired,
          correct: bool.isRequired,
          feedback: string.isRequired,
        })
      ),
    }).isRequired,
  }).isRequired,
  subject: shape({
    name: string.isRequired,
    entityId: string.isRequired,
  }).isRequired,
  body: shape({
    choice: string,
    seed: string,
  }),
}

LearnChoiceCardPage.defaultProps = {
  learned: null,
  body: {
    choice: null,
    seed: undefined,
  },
}
