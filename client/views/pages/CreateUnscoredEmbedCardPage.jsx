import React from 'react'
import { string, shape } from 'prop-types'
import ReactMarkdown from 'react-markdown'
import Layout from '../components/Layout'
import Icon from '../components/Icon'
import FormErrorsTop from '../components/FormErrorsTop'
import FormErrorsField from '../components/FormErrorsField'

export default function CreateUnscoredEmbedCardPage({
  hash,
  role,
  query: { subjectId },
  subject: { name: subjectName, body: subjectBody },
  body: { name, data$url },
  gqlErrors,
}) {
  return (
    <Layout
      hash={hash}
      page="CreateUnscoredEmbedCardPage"
      title={`Create an embed card for ${subjectName}`}
      description={`Help us build Sagefy by making a embed card for ${subjectName}.`}
    >
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />
      <header className="my-c">
        <p>
          <em>
            Great, an embed card! <Icon i="embed" />
          </em>
        </p>
        <h1 className="d-ib">
          Make a new embed card <Icon i="card" s="h1" />
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
          <input type="hidden" name="kind" value="UNSCORED_EMBED" />
          <p>
            <label htmlFor="name">What should we call this new card?</label>
            <input
              type="text"
              value={name}
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
              value={data$url}
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
              <Icon i="embed" /> Create Embed Card
            </button>
          </p>
        </form>
      </section>

      {role === 'sg_anonymous' && (
        <section>
          <p>
            <em>
              Advice: We recommend{' '}
              <a href={`/sign-up?return=/create-card?subjectId=${subjectId}`}>
                joining
              </a>{' '}
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

CreateUnscoredEmbedCardPage.propTypes = {
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
    data$url: string,
  }),
  gqlErrors: shape({}),
}

CreateUnscoredEmbedCardPage.defaultProps = {
  role: 'sg_anonymous',
  query: {
    subjectId: '',
    kind: '',
    name: '',
  },
  body: {
    name: '',
    data$url: '',
  },
  gqlErrors: {},
}
