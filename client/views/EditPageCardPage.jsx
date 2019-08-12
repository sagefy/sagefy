import React from 'react'
import { string, shape } from 'prop-types'
import ReactMarkdown from 'react-markdown'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import ExternalLink from './components/ExternalLink'
import FormErrorsTop from './components/FormErrorsTop'
import FormErrorsField from './components/FormErrorsField'
import Advice from './components/Advice'

export default function EditPageCardPage({
  hash,
  role,
  subject: { entityId: subjectId, name: subjectName, body: subjectBody },
  card: {
    entityId: cardId,
    name: prevName,
    data: { body: prevBody },
  },
  body: { name: bodyName, data$body: bodyBody },
  gqlErrors,
}) {
  return (
    <Layout
      hash={hash}
      page="EditPageCardPage"
      title={`Edit a choice page for ${subjectName}`}
      description={`Help us build Sagefy by updating a written document page card for ${subjectName}.`}
      canonical={`/page-cards/${to58(cardId)}`}
    >
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />
      <header className="my-c">
        <p>
          <em>
            Ready for change? <Icon i="page" />
          </em>
        </p>
        <h1 className="d-ib">
          Edit a page card <Icon i="card" s="h1" />
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
          <input type="hidden" name="kind" value="PAGE" />
          <p>
            <label htmlFor="name">What should we call this card?</label>
            <input
              type="text"
              value={bodyName || prevName}
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
              value={bodyBody || prevBody}
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
              <Icon i="page" /> Edit Page Card
            </button>
          </p>
        </form>
      </section>

      <Advice returnUrl={`/page-cards/${to58(cardId)}/edit`} role={role} />
    </Layout>
  )
}

EditPageCardPage.propTypes = {
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
      body: string.isRequired,
    }).isRequired,
  }).isRequired,
  body: shape({
    name: string,
    data$body: string,
  }),
  gqlErrors: shape({}),
}

EditPageCardPage.defaultProps = {
  role: 'sg_anonymous',
  body: {
    name: '',
    data$body: '',
  },
  gqlErrors: {},
}
