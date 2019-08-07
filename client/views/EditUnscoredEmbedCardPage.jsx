import React from 'react'
import { string, shape } from 'prop-types'
import ReactMarkdown from 'react-markdown'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import FormErrorsTop from './components/FormErrorsTop'
import FormErrorsField from './components/FormErrorsField'

export default function EditUnscoredEmbedCardPage({
  hash,
  role,
  subject: { entityId: subjectId, name: subjectName, body: subjectBody },
  card: {
    entityId: cardId,
    name: prevName,
    data: { url: prevUrl },
  },
  body: { name: bodyName, data$url: bodyUrl },
  gqlErrors,
}) {
  return (
    <Layout
      hash={hash}
      page="EditUnscoredEmbedCardPage"
      title={`Edit an embed card for ${subjectName}`}
      description={`Help us build Sagefy by updating a embed card for ${subjectName}.`}
      canonical={`/unscored-embed-cards/${to58(cardId)}`}
    >
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />
      <header className="my-c">
        <p>
          <em>
            Ready for change? <Icon i="embed" />
          </em>
        </p>
        <h1 className="d-ib">
          Edit an embed card <Icon i="card" s="h1" />
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
          <input type="hidden" name="kind" value="UNSCORED_EMBED" />
          <p>
            <label htmlFor="name">What should we call this card?</label>
            <input
              type="text"
              value={bodyName || prevName}
              placeholder="example: Label the guitar parts"
              size="40"
              id="name"
              name="name"
              autoFocus
            />
          </p>
          <FormErrorsField formErrors={gqlErrors} field="name" />
          <p>
            <label htmlFor="data$url">Where is the embed?</label>
            <input
              type="url"
              value={bodyUrl || prevUrl}
              placeholder="example: https://sgfy.xyz/ampvol"
              size="40"
              id="data$url"
              name="data$url"
            />
            <br />
            <small>
              We include the embed as <code>600x400</code>.
            </small>
          </p>
          <FormErrorsField formErrors={gqlErrors} field="data$url" />
          <p>
            <button type="submit">
              <Icon i="embed" /> Edit Embed Card
            </button>
          </p>
        </form>
      </section>

      {role === 'sg_anonymous' && (
        <section>
          <p>
            <em>
              Advice: We recommend{' '}
              <a
                href={`/sign-up?return=/unscored-embed-cards/${to58(
                  cardId
                )}/edit`}
              >
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

EditUnscoredEmbedCardPage.propTypes = {
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
      url: string.isRequired,
    }).isRequired,
  }).isRequired,
  body: shape({
    name: string,
    data$url: string,
  }),
  gqlErrors: shape({}),
}

EditUnscoredEmbedCardPage.defaultProps = {
  role: 'sg_anonymous',
  body: {
    name: '',
    data$url: '',
  },
  gqlErrors: {},
}
