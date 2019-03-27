import React from 'react'
import { string, arrayOf, shape } from 'prop-types'
import Icon from '../components/Icon'
import Footer from '../components/Footer'
import ChooseSubject from '../components/ChooseSubject'

export default function SearchSubjectsPage({
  role,
  query: { q },
  searchSubjects,
}) {
  return (
    <div className="SearchSubjectsPage">
      <section className="text-align-center">
        <h1>
          What do you want to learn? <Icon i="search" s="xxl" />
        </h1>
        <form action="/search-subjects">
          <p>
            <input
              type="search"
              size="40"
              value={q}
              placeholder="example: Music"
              autoFocus={!!q}
              name="q"
            />
          </p>
          <p>
            <button type="submit">
              <Icon i="search" /> Search
            </button>
          </p>
        </form>
      </section>

      {(searchSubjects && searchSubjects.nodes.length && (
        <section>
          <h2>
            Choose from one of these subjects <Icon i="subject" s="xl" />
          </h2>
          <ChooseSubject subjects={searchSubjects.nodes} />
        </section>
      )) ||
        null}

      {q && (
        <section>
          <h2>
            Not seeing what you want? <Icon i="error" s="xl" />
          </h2>
          <p>
            Right now Sagefy is temporarily limited. Soon you&apos;ll be able to
            suggest a new subject right here! Stay tuned.
          </p>
        </section>
      )}

      {/* TODO when !q, show popular subjects here */}

      {/*
        TODO once you can create a subject...
      <section>
        <p><mark>🤷🏽‍♀️ Not seeing what you want? 🤷🏽‍♀️</mark></p>

        {/* alternative: Looking for something else? (if no search) *
        {/* alternative:  (if couldn't find anything) *

        <details>
          <summary><h2 class="display-inline-block">You can suggest a new subject 💡</h2></summary>

          <form action="/create-subject">
            <p>
              <label for="name">What should we call this new subject?</label>
              <input type="text" value="Music" placeholder="example: Introduction to Classical Guitar" size="40" id="name" name="name" autofocus />
            </p>

            <p>
              <label for="body">What are the goals of this subject?</label>
              <textarea placeholder="example: An introduction to classical guitar. Let's learn some chords. And how to read guitar tablature." cols="40" rows="4" id="body" name="body"></textarea>
            </p>

            {/*
              If the user isn't logged in, ask them to (optionally) sign up to get notified
            *
            <p>
              <em>Advice: We recommend <a href="/sign-up?return=/create-subject">joining</a> before you create content,<br />
              so you can easily continue later!</em>
            </p>

            <p>
              <button type="submit">📚 Create Subject</button>
            </p>
          </form>

        </details>

      </section>
      */}

      <Footer role={role} />
    </div>
  )
}

SearchSubjectsPage.propTypes = {
  role: string,
  query: shape({}).isRequired,
  searchSubjects: arrayOf(shape({})),
}

SearchSubjectsPage.defaultProps = {
  role: 'sg_anonymous',
  searchSubjects: null,
}
