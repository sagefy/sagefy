/* eslint-disable camelcase */
import React from 'react'
import { string, shape } from 'prop-types'
import ReactMarkdown from 'react-markdown'
import toPairs from 'lodash.topairs'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import ExternalLink from './components/ExternalLink'
import FormErrorsTop from './components/FormErrorsTop'
import FormErrorsField from './components/FormErrorsField'

export default function ChoiceCardEditPage({
  hash,
  role,
  subject: { entityId: subjectId, name: subjectName, body: subjectBody },
  card: {
    entityId: cardId,
    name: prevName,
    data: { options: prevOptions },
  },
  body: { name: bodyName, options: bodyOptions },
  gqlErrors,
}) {
  const options = bodyOptions || prevOptions
  return (
    <Layout
      hash={hash}
      page="ChoiceCardEditPage"
      title={`Edit a choice card for ${subjectName}`}
      description={`Help us build Sagefy by updating a multiple choice card for ${subjectName}.`}
    >
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />
      <header className="my-c">
        <p>
          <em>
            Ready for change? <Icon i="choice" />
          </em>
        </p>
        <h1 className="d-ib">
          Edit a choice card <Icon i="card" s="h1" />
        </h1>
        <details>
          <summary>
            <span>
              <em>for the subject:</em> <h3 className="d-i">{subjectName}</h3>
            </span>
          </summary>
          <ReactMarkdown source={subjectBody} disallowedTypes={['heading']} />
        </details>
      </header>
      <section>
        <form method="POST">
          <input type="hidden" name="subjectId" value={to58(subjectId)} />
          <input type="hidden" name="kind" value="CHOICE" />
          <input type="hidden" name="data$max_options_to_show" value="4" />
          <p>
            <label htmlFor="name">What is the question?</label>
            <textarea
              value={bodyName || prevName}
              placeholder="example: How many string are there on a guitar?"
              id="name"
              name="name"
              cols="40"
              rows="4"
            />
            <br />
            <small>
              This field allows{' '}
              <ExternalLink href="https://www.markdownguide.org/cheat-sheet">
                Markdown
              </ExternalLink>{' '}
              format.
            </small>
          </p>
          <FormErrorsField formErrors={gqlErrors} field="name" />
          <h3>Options</h3>
          <table>
            <thead>
              <tr>
                <th>OK</th>
                <th>Value</th>
                <th>Feedback</th>
              </tr>
            </thead>
            {toPairs(options).map(([key, { correct, value, feedback }], i) => (
              <tr>
                <td className="ta-c va-m">
                  <input
                    type="radio"
                    name="data$correct"
                    value={key}
                    checked={correct}
                  />
                </td>
                <td>
                  <textarea
                    rows="2"
                    placeholder={
                      i === 0 && 'example: A guitar has six strings. '
                    }
                    value={value}
                    id={`data$options$${key}$value`}
                    name={`data$options$${key}$value`}
                  />
                </td>
                <td>
                  <textarea
                    rows="2"
                    placeholder={i === 0 && 'example: Great work!'}
                    value={feedback}
                    id={`data$options$${key}$feedback`}
                    name={`data$options$${key}$feedback`}
                  />
                </td>
              </tr>
            ))}
          </table>
          <FormErrorsField formErrors={gqlErrors} field="data$options" />
          <p>
            <small>
              The value and feedback here allows{' '}
              <ExternalLink href="https://www.markdownguide.org/cheat-sheet">
                Markdown
              </ExternalLink>
              .
            </small>
          </p>
          <p>
            <button type="submit">
              <Icon i="choice" /> Edit Choice Card
            </button>
          </p>
        </form>
      </section>

      {role === 'sg_anonymous' && (
        <section>
          <p>
            <em>
              Advice: We recommend{' '}
              <a href={`/sign-up?return=/choice-cards/${to58(cardId)}/edit`}>
                joining
              </a>{' '}
              before you edit content,
              <br />
              so you can easily continue later!
            </em>
          </p>
        </section>
      )}
    </Layout>
  )
}

ChoiceCardEditPage.propTypes = {
  hash: string.isRequired,
  role: string,
  subject: shape({
    entityId: string.isRequired,
    name: string.isRequired,
    body: string.isRequired,
  }).isRequired,
  card: shape({
    entityId: string.isRequired,
    name: string.isRequired,
    data: shape({
      options: shape({}).isRequired,
    }).isRequired,
  }).isRequired,
  body: shape({
    name: string,
    options: shape({}),
  }),
  gqlErrors: shape({}),
}

ChoiceCardEditPage.defaultProps = {
  role: 'sg_anonymous',
  body: {
    name: '',
  },
  gqlErrors: {},
}
