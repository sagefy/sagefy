/* eslint-disable camelcase */
import React from 'react'
import { string, shape } from 'prop-types'
import ReactMarkdown from 'react-markdown'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import FormErrorsTop from './components/FormErrorsTop'
import FormErrorsField from './components/FormErrorsField'
import Advice from './components/Advice'

export default function EditVideoCardPage({
  hash,
  role,
  subject: { entityId: subjectId, name: subjectName, body: subjectBody },
  card: {
    entityId: cardId,
    name: prevName,
    data: { video_id: prevVideoId, site: prevSite },
  },
  body: { name: bodyName, data$video_id: bodyVideoId, data$site: bodySite },
  gqlErrors,
}) {
  return (
    <Layout
      hash={hash}
      page="EditVideoCardPage"
      title={`Edit a video card for ${subjectName}`}
      description={`Help us build Sagefy by updating a video card for ${subjectName}.`}
      canonical={`/video-cards/${to58(cardId)}`}
    >
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />
      <header className="my-c">
        <p>
          <em>
            Ready for change? <Icon i="video" />
          </em>
        </p>
        <h1 className="d-ib">
          Edit a video card <Icon i="card" s="h1" />
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
          <input type="hidden" name="kind" value="VIDEO" />
          <p>
            <label htmlFor="name">What should we call this card?</label>
            <input
              type="text"
              value={bodyName || prevName}
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
                      name="data$site"
                      value="youtube"
                      checked={(bodySite || prevSite) === 'youtube'}
                    />{' '}
                    <code>https://youtube.com/watch?v=</code>
                  </label>
                </td>
                <td rowSpan="2">
                  <input
                    type="text"
                    value={bodyVideoId || prevVideoId}
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
                    <input
                      type="radio"
                      name="data$site"
                      value="vimeo"
                      checked={(bodySite || prevSite) === 'vimeo'}
                    />{' '}
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
              <Icon i="video" /> Edit Video Card
            </button>
          </p>
        </form>
      </section>

      <Advice returnUrl={`/video-cards/${to58(cardId)}/edit`} role={role} />
    </Layout>
  )
}

EditVideoCardPage.propTypes = {
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
      video_id: string.isRequired,
      site: string.isRequired,
    }).isRequired,
  }).isRequired,
  body: shape({
    name: string,
    data$video_id: string,
    data$site: string,
  }),
  gqlErrors: shape({}),
}

EditVideoCardPage.defaultProps = {
  role: 'sg_anonymous',
  body: {
    name: '',
    data$video_id: '',
    data$site: '',
  },
  gqlErrors: {},
}
