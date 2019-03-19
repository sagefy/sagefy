import React from 'react'
// import { Link } from 'react-router-dom'
import { string } from 'prop-types'
import Icon from '../components/Icon'
import Footer from '../components/Footer'

export default function DashboardPage({ role }) {
  return (
    <div className="DashboardPage">
      <section>
        <h1>
          Welcome to Sagefy <Icon i="dashboard" s="xxl" />
        </h1>
        <p>
          I&apos;ve reserved your user name and password! That said, there
          isn&apos;t much to do right now.
        </p>
      </section>

      <Footer role={role} />
    </div>
  )
}

DashboardPage.propTypes = {
  role: string,
}

DashboardPage.defaultProps = {
  role: 'sg_anonymous',
}

/*
      <section className="collapse-margins">
        <p>
          <em>Hi Doris, welcome back!</em>
        </p>{' '}
        {/* TODO copy should change based on state *}
        <h1>
          What do you want to learn?{' '}
          <img src="/astrolabe.svg" height="32" alt="astrolabe" />
        </h1>
      </section>

      TODO If the user has no subjects, then list popular subjects here instead
      TODO implement
      <section>
        <h2>
          Choose one of your subjects <Icon i="subject" s="xl" />
        </h2>
        <table>
          <tr>
            <td className="text-align-center collapse-margins">
              <p>
                <button type="submit">
                  <Icon i="up" />
                </button>
              </p>
              <code>15%</code>
            </td>
            <td className="collapse-margins">
              <h3>
                <mark>
                  <Link to="/choose-next">
                    An Introduction to Electronic Music
                  </Link>
                </mark>
              </h3>
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
              <code>0%</code>
            </td>
            <td className="collapse-margins">
              <h3>
                <Link to="/choose-next">Lets Play Classical Guitar</Link>
              </h3>
              <p>
                An introduction to classical guitar. Lets learn some chords. And
                how to read guitar tabulature.
              </p>
            </td>
          </tr>
          <tr>
            <td className="collapse-margins" colSpan="2">
              <h3>
                ...or how about something else? <Icon i="search" s="l" />
              </h3>
              <form action="/search-subjects">
                <input type="search" size="40" placeholder="example: Music" />
                <button type="submit">
                  <Icon i="search" /> Search
                </button>
              </form>
            </td>
          </tr>
        </table>
      </section>


<section>
  <h2>You've got some new notices 🔔</h2>
  <ul className="list-style-none">
    <li>
      <p>
        Eileen voted ✅ yes on your proposal on
        <a href="/talk">Music Theory</a>.
      </p>
    </li>
    <li>
      <p>
        Or,
        <strong><a href="/notices">🔔 See all your notices</a>.</strong>
      </p>
    </li>
  </ul>
</section>

<section>
  <h2>Help us build Sagefy 🌳</h2>

  <details>
    <summary><h3 className="display-inline-block">Add some cards 🃏</h3></summary>
    <ul>
      <li>
        <a href="/create-card"
          >Add cards to 🎧 <em>An Introduction to Electronic Music</em></a
        >
        <small>(0 cards)</small>
      </li>
      <li>
        <a href="/create-card"
          >Add cards to 🎸 <em>Let's Play Classical Guitar</em></a
        >
        <small>(10 cards)</small>
      </li>
      {/* prioritized queue, descend children of followed subjects *}
    </ul>
  </details>

  <details>
    <summary
      ><h3 className="display-inline-block">
        You can make a new subject 💡
      </h3></summary
    >

    <form action="/mocks/create-subject">
      <p>
        <label for="name">What should we call this new subject?</label>
        <input
          type="text"
          value="Music"
          placeholder="example: Introduction to Classical Guitar"
          size="40"
          id="name"
          name="name"
          autofocus
        />
      </p>

      <p>
        <label for="body">What are the goals of this subject?</label>
        <textarea
          placeholder="example: An introduction to classical guitar. Let's learn some chords. And how to read guitar tablature."
          cols="40"
          rows="4"
          id="body"
          name="body"
        ></textarea>
      </p>

      <p>
        <button type="submit">📚 Create Subject</button>
      </p>
    </form>
  </details>

  <details>
    <summary
      ><h3 className="display-inline-block">
        ...or find something else 🕵🏻‍♀️
      </h3></summary
    >
    <form action="/mocks/search">
      <input type="search" size="40" placeholder="example: Music" />
      <button type="submit">🕵🏻‍♀️ Search</button>
    </form>
  </details>
</section>

<section>
  <details>
    <summary>
      <span>🤷🏽‍♀️ What are cards &amp; subjects? 🤷🏽‍♀️</span>
    </summary>
    <ul>
      <li>
        <p>A <strong>card</strong> is a single learning activity. 🃏</p>
        <blockquote>
          <p>Examples: a 3-minute video or a multiple choice question.</p>
        </blockquote>
      </li>
      <li>
        <p>
          A <strong>subject</strong> is a collection of cards and other
          subjects. 📚
        </p>
        <blockquote>
          <p>
            Like a course, but at any scale. Such as “Measures of Central
            Tendency”, “Intro to Statistics”, or even a complete statistics
            program.
          </p>
        </blockquote>
      </li>
    </ul>
  </details>
</section>
*/
