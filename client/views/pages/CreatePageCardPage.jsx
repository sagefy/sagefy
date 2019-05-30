import React from 'react'
import { string, shape } from 'prop-types'
import ReactMarkdown from 'react-markdown'
import { Link } from 'react-router-dom'
import Layout from '../components/Layout'
import Icon from '../components/Icon'
import ExternalLink from '../components/ExternalLink'
import FormErrorsTop from '../components/FormErrorsTop'
import FormErrorsField from '../components/FormErrorsField'

export default function CreatePageCardPage({
  hash,
  role,
  query: { subjectId },
  subject: { name: subjectName, body: subjectBody },
  body: { name, data$body },
  gqlErrors,
}) {
  return (
    <Layout
      hash={hash}
      page="CreatePageCardPage"
      title={`Create a choice page for ${subjectName}`}
      description={`Help us build Sagefy by making a written document page card for ${subjectName}.`}
    >
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />
      <header className="my-c">
        <p>
          <em>
            Great, a page card! <Icon i="page" />
          </em>
        </p>
        <h1 className="d-ib">
          Make a new page card <Icon i="card" s="h1" />
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
          <input type="hidden" name="subjectId" value={subjectId} />
          <input type="hidden" name="kind" value="PAGE" />
          <p>
            <label htmlFor="name">What should we call this new card?</label>
            <input
              type="text"
              value={name}
              placeholder="example: The parts of a guitar"
              size="40"
              id="name"
              name="name"
              autoFocus
            />
            <br />
            <small>
              This field will appear as an <code>h1</code>.
            </small>
          </p>
          <FormErrorsField formErrors={gqlErrors} field="name" />
          <p>
            <label htmlFor="data$body">Write your page</label>
            <textarea
              value={data$body}
              placeholder="example: A guitar has six strings, a headstock, a nut, frets, a neck, a body, a bridge, a sound hole..."
              id="data$body"
              name="data$body"
              className="w-100"
              rows="8"
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
          <FormErrorsField formErrors={gqlErrors} field="data$body" />
          <p>
            <button type="submit">
              <Icon i="page" /> Create Page Card
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

CreatePageCardPage.propTypes = {
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
    data$body: string,
  }),
  gqlErrors: shape({}),
}

CreatePageCardPage.defaultProps = {
  role: 'sg_anonymous',
  query: {
    subjectId: '',
    kind: '',
    name: '',
  },
  body: {
    name: '',
    data$body: '',
  },
  gqlErrors: {},
}
