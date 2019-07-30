import React from 'react'
import { string, shape } from 'prop-types'
import ReactMarkdown from 'react-markdown'
import Layout from './components/Layout'
import Icon from './components/Icon'

export default function CreateCardPage({
  role,
  query: { subjectId },
  subject: { name: subjectName, body: subjectBody },
  hash,
}) {
  const kindLink = kind => `/${kind}-cards/create?subjectId=${subjectId}`
  return (
    <Layout
      hash={hash}
      page="CreateCardPage"
      title={`Create Card for ${subjectName}`}
      description={`Help Sagefy grow by helping us make new cards for ${subjectName}`}
      canonical={`/subjects/${subjectId}`}
    >
      <header className="my-c">
        <p>
          <em>
            Let&apos;s learn by teaching <Icon i="build" /> and&hellip;
          </em>
        </p>
        <h1 className="d-ib">
          Make a new card <Icon i="card" s="h1" />
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
        <h2>What kind of card would you like to make?</h2>
        <ul className="ls-n">
          <li>
            <a href={kindLink('choice')}>
              <Icon i="choice" /> Choice
            </a>{' '}
            &ndash; A multiple-choice question.{' '}
            <em>
              <small>(We need more of these!)</small>
            </em>
          </li>
          <li>
            <a href={kindLink('page')}>
              <Icon i="page" /> Page
            </a>{' '}
            &ndash; A written document to read, in Markdown format.{' '}
            <em>
              <small>(This one&apos;s the easiest.)</small>
            </em>
          </li>
          <li>
            <a href={kindLink('video')}>
              <Icon i="video" /> Video
            </a>{' '}
            &ndash; A YouTube or Vimeo video.
          </li>
          <li>
            <a href={kindLink('unscored-embed')}>
              <Icon i="embed" /> Embed{' '}
            </a>{' '}
            &ndash; An <code>iframe</code> from any site. Does not score learner
            responses.
          </li>
        </ul>
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

CreateCardPage.propTypes = {
  hash: string.isRequired,
  role: string,
  query: shape({
    subjectId: string,
  }),
  subject: shape({
    name: string.isRequired,
    body: string.isRequired,
  }).isRequired,
}

CreateCardPage.defaultProps = {
  role: 'sg_anonymous',
  query: {
    subjectId: '',
    kind: '',
    name: '',
  },
}
