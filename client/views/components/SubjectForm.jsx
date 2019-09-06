import React from 'react'
import { string, shape } from 'prop-types'
import get from 'lodash.get'
import { to58 } from 'uuid58'
import Icon from './Icon'
import FormErrorsTop from './FormErrorsTop'
import FormErrorsField from './FormErrorsField'
import Advice from './Advice'

function findFirstValue(objs, field) {
  return objs.map(obj => get(obj, field)).find(Boolean)
}

export default function SubjectForm({
  form = {},
  preset = {},
  url = '/subjects/create',
  role,
  gqlErrors,
}) {
  const MODE = url.endsWith('edit') ? 'edit' : 'create'
  return (
    <form className="SubjectForm" action={url} method="POST">
      <FormErrorsTop formErrors={gqlErrors} />
      <FormErrorsField formErrors={gqlErrors} field="all" />

      {MODE === 'edit' && (
        <input type="hidden" name="entityId" value={to58(preset.entityId)} />
      )}

      <p>
        <label htmlFor="name">What should we call this new subject?</label>
        <input
          type="text"
          value={findFirstValue([form, preset], 'name')}
          placeholder="example: Introduction to Classical Guitar"
          size="40"
          id="name"
          name="name"
          autoFocus
          required
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
          value={findFirstValue([form, preset], 'body')}
          required
        />
      </p>
      <FormErrorsField formErrors={gqlErrors} field="body" />

      <p>
        <button type="submit">
          <Icon i={MODE} />{' '}
          {MODE === 'edit' ? 'Edit Subject' : 'Create Subject'}
        </button>
      </p>

      <Advice returnUrl={url} role={role} />
    </form>
  )
}

SubjectForm.propTypes = {
  form: shape({
    name: string,
    body: string,
  }),
  preset: shape({
    name: string,
    body: string,
  }),
  url: string,
  role: string,
  gqlErrors: shape({}),
}

SubjectForm.defaultProps = {
  form: {
    name: '',
    body: '',
  },
  preset: {
    name: '',
    body: '',
  },
  url: '/subjects/create',
  role: 'sg_anonymous',
  gqlErrors: {},
}
