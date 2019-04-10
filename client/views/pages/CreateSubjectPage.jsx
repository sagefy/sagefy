import React from 'react'
import { string, shape } from 'prop-types'
import Icon from '../components/Icon'
import CreateSubject from '../components/CreateSubject'

export default function CreateSubjectPage({
  role,
  body: { name, body } = {},
  gqlErrors,
}) {
  return (
    <div className="CreateSubjectPage">
      <section>
        <h1>
          Let&apos;s make a new subject! <Icon i="subject" s="xxl" />
        </h1>
        <CreateSubject
          role={role}
          name={name}
          body={body}
          gqlErrors={gqlErrors}
        />
      </section>
    </div>
  )
}

CreateSubjectPage.propTypes = {
  role: string.isRequired,
  body: shape({}),
  gqlErrors: shape({}),
}

CreateSubjectPage.defaultProps = {
  body: {},
  gqlErrors: {},
}
