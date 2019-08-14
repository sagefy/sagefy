import React from 'react'
import { string, shape } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import SubjectForm from './components/SubjectForm'

export default function EditSubjectPage({
  hash,
  role,
  body,
  subject = {},
  gqlErrors,
}) {
  return (
    <Layout
      hash={hash}
      page="EditSubjectPage"
      title="Edit subject"
      description="Help Sagefy grow by editing an existing subject! Anyone can edit a subject, no account required."
      canonical={`/subjects/${to58(subject.entityId)}`}
    >
      <section>
        <h1>
          Let&apos;s edit an existing subject! <Icon i="subject" s="h1" />
        </h1>
        <SubjectForm
          form={body}
          preset={subject}
          url={`/subjects/${to58(subject.entityId)}/edit`}
          role={role}
          gqlErrors={gqlErrors}
        />
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
