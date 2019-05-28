/* eslint-disable camelcase */
import React from 'react'
import { string, shape } from 'prop-types'
import ReactMarkdown from 'react-markdown'
import { Link } from 'react-router-dom'
import Layout from '../components/Layout'
import Icon from '../components/Icon'
import FormErrorsTop from '../components/FormErrorsTop'
import FormErrorsField from '../components/FormErrorsField'

export default function CreateVideoCardPage({
  hash,
  role,
  query: { subjectId },
  subject: { name: subjectName, body: subjectBody },
  body: { name, data$video_id },
  gqlErrors,
}) {
  return (
    <Layout
      hash={hash}
      page="CreateVideoCardPage"
      title={`Create a video card for ${subjectName}`}
      description={`Help us build Sagefy by making a video card for ${subjectName}.`}
    >
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />
      <header className="m-yc">
        <p>
          <em>
            Great, a video card! <Icon i="video" />
          </em>
        </p>
        <h1 className="d-ib">
          Make a new video card <Icon i="card" s="h1" />
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
          <input type="hidden" name="kind" value="VIDEO" />
          <input type="hidden" name="data.site" value="youtube" />
          <p>
            <label htmlFor="name">What should we call this new card?</label>
            <input
              type="text"
              value={name}
              placeholder="example: A clip on guitar anatomy"
              size="40"
              id="name"
              name="name"
              autoFocus
            />
          </p>
          <FormErrorsField formErrors={gqlErrors} field="name" />
          <p>
            <label htmlFor="data$video_id">
              What is the ID of the YouTube video?
            </label>
            <code>https://youtube.com/watch?v=</code>{' '}
            <input
              type="text"
              value={data$video_id}
              size="15"
              id="data$video_id"
              name="data$video_id"
              placeholder="ex: Gi99QbiSuWs"
            />
            <br />
            <small>We recommend videos no longer than five minutes.</small>
          </p>
          <FormErrorsField formErrors={gqlErrors} field="data$video_id" />
          <p>
            <button type="submit">
              <Icon i="video" /> Create Video Card
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

CreateVideoCardPage.propTypes = {
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
    data$video_id: string,
  }),
  gqlErrors: shape({}),
}

CreateVideoCardPage.defaultProps = {
  role: 'sg_anonymous',
  query: {
    subjectId: '',
    kind: '',
    name: '',
  },
  body: {
    name: '',
    data$video_id: '',
  },
  gqlErrors: {},
}
