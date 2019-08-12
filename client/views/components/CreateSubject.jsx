import React from 'react'
import { string, shape } from 'prop-types'
import Icon from './Icon'
import FormErrorsTop from './FormErrorsTop'
import FormErrorsField from './FormErrorsField'
import Advice from './Advice'

export default function CreateSubject({
  name: inputName,
  body: { name, body },
  role,
  gqlErrors,
}) {
  return (
    <form className="CreateSubject" action="/subjects/create" method="POST">
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />

      <p>
        <label htmlFor="name">What should we call this new subject?</label>
        <input
          type="text"
          value={name || inputName}
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
          value={body}
        />
      </p>
      <FormErrorsField formErrors={gqlErrors} field="body" />

      <p>
        <button type="submit">
          <Icon i="search" /> Create Subject
        </button>
      </p>

      <Advice returnUrl="/subjects/create" role={role} />
    </form>
  )
}

CreateSubject.propTypes = {
  name: string,
  body: shape({
    name: string,
    body: string,
  }),
  role: string.isRequired,
  gqlErrors: shape({}),
}

CreateSubject.defaultProps = {
  name: '',
  body: {
    name: '',
    body: '',
  },
  gqlErrors: {},
}
