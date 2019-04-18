/* eslint-disable camelcase */
import React from 'react'
import { string, shape } from 'prop-types'
import ReactMarkdown from 'react-markdown'
import { Link } from 'react-router-dom'
import get from 'lodash.get'
import Layout from '../components/Layout'
import Icon from '../components/Icon'
import ExternalLink from '../components/ExternalLink'
import FormErrorsTop from '../components/FormErrorsTop'
import FormErrorsField from '../components/FormErrorsField'

export default function CreateChoiceCardPage({
  hash,
  role,
  query: { subjectId },
  subject: { name: subjectName, body: subjectBody },
  body: { name, ...reqBody },
  gqlErrors,
}) {
  return (
    <Layout
      hash={hash}
      page="CreateChoiceCardPage"
      title={`Create a choice card for ${subjectName}`}
      description={`Help us build Sagefy by making a multiple choice card for ${subjectName}.`}
    >
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />
      <header className="m-yc">
        <p>
          <em>
            Great, a choice card! <Icon i="choice" />
          </em>
        </p>
        <h1 className="d-ib">
          Make a new choice card <Icon i="card" s="h1" />
        </h1>{' '}
        <p className="d-ib">
          <em>for the subject&hellip;</em>
        </p>
        <blockquote className="m-yc">
          <h3>{subjectName}</h3>
          <ReactMarkdown source={subjectBody} disallowedTypes={['heading']} />
        </blockquote>
      </header>
      <section>
        <form method="POST">
          <input type="hidden" name="subjectId" value={subjectId} />
          <input type="hidden" name="kind" value="CHOICE" />
          <input type="hidden" name="data$max_options_to_show" value="4" />
          <p>
            <label htmlFor="name">What is the question?</label>
            <textarea
              value={name}
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
            {[0, 1, 2, 3].map(i => (
              <tr>
                <td className="ta-c va-m">
                  <input type="radio" name="data$correct" value={i} />
                </td>
                <td>
                  <textarea
                    rows="2"
                    placeholder={
                      i === 0 && 'example: A guitar has six strings. '
                    }
                    value={get(reqBody, `data$options$${i}$value`)}
                    id={`data$options$${i}$value`}
                    name={`data$options$${i}$value`}
                  />
                </td>
                <td>
                  <textarea
                    rows="2"
                    placeholder={i === 0 && 'example: Great work!'}
                    value={get(reqBody, `data$options$${i}$feedback`)}
                    id={`data$options$${i}$feedback`}
                    name={`data$options$${i}$feedback`}
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
              <Icon i="choice" /> Create Choice Card
            </button>
          </p>
        </form>
      </section>

      {role === 'sg_anonymous' && (
        <section>
          <p>
            <em>
              Advice: We recommend{' '}
              <Link to={`/sign-up?return=/create-card?subjectId=${subjectId}`}>
                joining
              </Link>{' '}
              before you create content,
              <br />
              so you can easily continue later!
            </em>
          </p>
        </section>
      )}
    </Layout>
  )
}

CreateChoiceCardPage.propTypes = {
  hash: string.isRequired,
  role: string,
  query: shape({
    subjectId: string,
  }),
  subject: shape({
    name: string.isRequired,
    body: string.isRequired,
  }).isRequired,
  body: shape({
    name: string,
  }),
  gqlErrors: shape({}),
}

CreateChoiceCardPage.defaultProps = {
  role: 'sg_anonymous',
  query: {
    subjectId: '',
    kind: '',
    name: '',
  },
  body: {
    name: '',
  },
  gqlErrors: {},
}
