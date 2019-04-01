import React from 'react'
import { string } from 'prop-types'
import Icon from './Icon'

export default function CreateSubject({ name, body, role }) {
  return (
    <form action="/create-subject" method="POST">
      <p>
        <label htmlFor="name">What should we call this new subject?</label>
        <input
          type="text"
          value={name}
          placeholder="example: Introduction to Classical Guitar"
          size="40"
          id="name"
          name="name"
          autoFocus
        />
      </p>

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

      {role === 'sg_anonymous' && (
        <p>
          <em>
            Advice: We recommend{' '}
            <a href="/sign-up?return=/create-subject">joining</a> before you
            create content,
            <br />
            so you can easily continue later!
          </em>
        </p>
      )}

      <p>
        <button type="submit">
          <Icon i="search" /> Create Subject
        </button>
      </p>
    </form>
  )
}

CreateSubject.propTypes = {
  name: string,
  body: string,
  role: string.isRequired,
}

CreateSubject.defaultProps = {
  name: '',
  body: '',
}
