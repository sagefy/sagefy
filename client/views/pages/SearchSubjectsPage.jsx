import React from 'react'
import { string, shape } from 'prop-types'
import Icon from '../components/Icon'
import Footer from '../components/Footer'
import ChooseSubject from '../components/ChooseSubject'
import CreateSubject from '../components/CreateSubject'

export default function SearchSubjectsPage({
  role,
  query: { q },
  searchSubjects,
}) {
  return (
    <div className="SearchSubjectsPage">
      <section className="ta-c">
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
          <p>
            <em>
              Not seeing what you want? <Icon i="error" />
            </em>
          </p>
          <details open={!searchSubjects || !searchSubjects.nodes.length}>
            <summary>
              <h2 className="d-i">
                You can suggest a new subject <Icon i="subject" s="xl" />
              </h2>
            </summary>

            <CreateSubject role={role} name={q} />
          </details>
        </section>
      )}

      {/* TODO when !q, show popular subjects here */}

      <Footer role={role} />
    </div>
  )
}

SearchSubjectsPage.propTypes = {
  role: string,
  query: shape({}).isRequired,
  searchSubjects: shape({}),
}

SearchSubjectsPage.defaultProps = {
  role: 'sg_anonymous',
  searchSubjects: null,
}
