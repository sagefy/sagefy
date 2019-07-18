/* eslint-disable camelcase */
import React from 'react'
import { string, shape } from 'prop-types'
import ReactMarkdown from 'react-markdown'
import Layout from './components/Layout'
import Icon from './components/Icon'
import FormErrorsTop from './components/FormErrorsTop'
import FormErrorsField from './components/FormErrorsField'

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
      <header className="my-c">
        <p>
          <em>
            Great, a video card! <Icon i="video" />
          </em>
        </p>
        <h1 className="d-ib">
          Make a new video card <Icon i="card" s="h1" />
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
          <input type="hidden" name="kind" value="VIDEO" />
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
              What is the site and ID of the video?
            </label>
            <table>
              <tr>
                <td>
                  <label>
                    <input
                      type="radio"
                      name="data.site"
                      value="youtube"
                      defaultChecked
                    />{' '}
                    <code>https://youtube.com/watch?v=</code>
                  </label>
                </td>
                <td rowSpan="2">
                  <input
                    type="text"
                    value={data$video_id}
                    size="15"
                    id="data$video_id"
                    name="data$video_id"
                    placeholder="ex: Gi99QbiSuWs"
                  />
                </td>
              </tr>
              <tr>
                <td>
                  <label>
                    <input type="radio" name="data.site" value="vimeo" />{' '}
                    <code>https://vimeo.com/</code>
                  </label>
                </td>
              </tr>
            </table>
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
              <a href={`/sign-up?return=/cards/create?subjectId=${subjectId}`}>
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
