import React from 'react'
import { string, shape } from 'prop-types'
import Icon from './Icon'
import FormErrorsTop from './FormErrorsTop'
import FormErrorsField from './FormErrorsField'

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

      {role === 'sg_anonymous' && (
        <p>
          <em>
            Advice: We recommend{' '}
            <a href="/sign-up?return=/subjects/create">joining</a> before you
            create content,
            <br />
            so you can easily continue later!
          </em>
        </p>
      )}
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
