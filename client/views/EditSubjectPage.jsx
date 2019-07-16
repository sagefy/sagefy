import React from 'react'
import { string, shape } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import FormErrorsTop from './components/FormErrorsTop'
import FormErrorsField from './components/FormErrorsField'

export default function EditSubjectPage({
  hash,
  role,
  body: { name: bodyName, body: bodyBody } = {},
  subject: { entityId, name: prevName, body: prevBody },
  gqlErrors,
}) {
  return (
    <Layout
      hash={hash}
      page="EditSubjectPage"
      title="Edit subject"
      description="Help Sagefy grow by editing an existing subject! Anyone can edit a subject, no account required."
    >
      <section>
        <h1>
          Let&apos;s edit an existing subject! <Icon i="subject" s="h1" />
        </h1>
        <form method="POST">
          <FormErrorsTop formErrors={gqlErrors} />
          <FormErrorsField formErrors={gqlErrors} field="all" />

          <input type="hidden" name="entityId" value={to58(entityId)} />

          <p>
            <label htmlFor="name">What should we call this new subject?</label>
            <input
              type="text"
              value={bodyName || prevName}
              placeholder="example: Introduction to Classical Guitar"
              size="40"
              id="name"
              name="name"
              autoFocus
            />
          </p>
          <FormErrorsField formErrors={gqlErrors} field="name" />

          <p>
            <label htmlFor="body">What are the goals of this subject?</label>
            <textarea
              placeholder="example: An introduction to classical guitar. Let's learn some chords. And how to read guitar tablature."
              cols="40"
              rows="4"
              id="body"
              name="body"
              value={bodyBody || prevBody}
            />
          </p>
          <FormErrorsField formErrors={gqlErrors} field="body" />

          <p>
            <button type="submit">
              <Icon i="edit" /> Edit Subject
            </button>
          </p>

          {role === 'sg_anonymous' && (
            <p>
              <em>
                Advice: We recommend{' '}
                <a href={`/sign-up?return=/subjects/${to58(entityId)}/edit`}>
                  joining
                </a>{' '}
                before you edit content,
                <br />
                so you can easily continue later!
              </em>
            </p>
          )}
        </form>
      </section>
    </Layout>
  )
}

EditSubjectPage.propTypes = {
  hash: string.isRequired,
  role: string.isRequired,
  body: shape({}),
  subject: shape({
    entityId: string.isRequired,
    name: string.isRequired,
    body: string.isRequired,
  }).isRequired,
  gqlErrors: shape({}),
}

EditSubjectPage.defaultProps = {
  body: {},
  gqlErrors: {},
}
