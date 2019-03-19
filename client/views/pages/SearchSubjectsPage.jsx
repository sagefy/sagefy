import React from 'react'
import { string } from 'prop-types'
// import { Link } from 'react-router-dom'
import Icon from '../components/Icon'
import Footer from '../components/Footer'

export default function SearchSubjectsPage({ role, q }) {
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
              autoFocus
            />
          </p>
          <p>
            <button type="submit">
              <Icon i="search" /> Search
            </button>
          </p>
        </form>
      </section>

      {/* Search results, if there are none ... whats the empty state? *}
      {/* TODO make real *}
      <section>
        <h2>
          Choose from one of these subjects <Icon i="subject" s="xl" />
        </h2>

        <table>
          <tr>
            <td className="text-align-center collapse-margins">
              <p>
                <button type="submit">
                  <Icon i="up" />
                </button>
              </p>
              <code>12</code>
            </td>
            <td className="collapse-margins">
              <h3>
                <mark>
                  <Link to="/choose-next">
                    An Introduction to Electronic Music
                  </Link>
                </mark>
              </h3>
              {/* If a subject doesn't have enough cards, suggest creating cards or just following instead. *}
              <p>
                A small taste of the basics of electronic music. Learn the
                concepts behind creating and modifying sounds in an electronic
                music system. Learn the ideas behind the tools and systems we
                use to create electronic music.
              </p>
            </td>
          </tr>
          <tr>
            <td className="text-align-center collapse-margins">
              <p>
                <button type="button">
                  <Icon i="up" />
                </button>
              </p>
              <code>12</code>
            </td>
            <td className="collapse-margins">
              <h3>
                <a href="/choose-next">Lets Play Classical Guitar</a>
              </h3>
              <p>
                An introduction to classical guitar. Lets learn some chords. And
                how to read guitar tabulature.
              </p>
            </td>
          </tr>
          <tr>
            <td className="text-align-center collapse-margins">
              <p>
                <button type="button">
                  <Icon i="up" />
                </button>
              </p>
              <code>12</code>
            </td>
            <td className="collapse-margins">
              <h3>
                <a href="/choose-next">Welcome to Music Theory</a>
              </h3>
              <p>
                Well cover the basics of how to read sheet music. Chords,
                progressions, and sequences. Harmony.
              </p>
            </td>
          </tr>
        </table>
      </section>


        TODO once you can create a subject...
      <section>
        <p><mark>🤷🏽‍♀️ Not seeing what you want? 🤷🏽‍♀️</mark></p>

        {/* alternative: Looking for something else? (if no search) *
        {/* alternative: We couldn't find anything (if couldn't find anything) *

        <details>
          <summary><h2 class="display-inline-block">You can make a new subject 💡</h2></summary>

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
  q: string,
}

SearchSubjectsPage.defaultProps = {
  role: 'sg_anonymous',
  q: '',
}
