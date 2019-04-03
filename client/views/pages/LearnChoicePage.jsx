/* eslint-disable camelcase */
import React from 'react'
import ReactMarkdown from 'react-markdown'
import { string, number, shape, objectOf, bool } from 'prop-types'
import { shuffle } from 'shuffle-seed'
import Icon from '../components/Icon'

export default function LearnChoicePage({
  progress,
  name,
  data: { body, max_options_to_show, options },
  choice,
  seed = process.env.NODE_ENV === 'test' ? '_' : Date.now().toString(36),
}) {
  const xoptions = shuffle(Object.entries(options), seed).slice(
    0,
    max_options_to_show
  )
  return (
    <div className="LearnChoicePage">
      {progress && (
        <section>
          <progress value={progress} />
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
    </div>
  )
}

LearnChoicePage.propTypes = {
  progress: number,
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
  choice: string,
  seed: string,
}

LearnChoicePage.defaultProps = {
  progress: null,
  choice: null,
  seed: undefined,
}
