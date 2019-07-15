import React from 'react'
import { string, shape, arrayOf } from 'prop-types'
import Layout from '../components/Layout'
import Icon from '../components/Icon'
import Footer from '../components/Footer'
import ChooseSubject from '../components/ChooseSubject'
import CardSubjectInfo from '../components/CardSubjectInfo'

export default function DashboardPage({ role, subjects, name, hash }) {
  return (
    <Layout hash={hash} page="DashboardPage" title="Dashboard" description="-">
      <section className="my-c">
        <p>
          <em>
            Hi {name}, welcome back! <Icon i="sagefy" />
          </em>
        </p>
        {/* TODO copy should change based on state */}
        <h1>
          What do you want to learn? <Icon i="dashboard" s="h1" />
        </h1>
      </section>

      {subjects && subjects.length ? (
        <section>
          <h2>
            Choose one of your subjects <Icon i="subject" s="h2" />
          </h2>
          <ChooseSubject subjects={subjects} level="goal" />
          <div className="my-c">
            <h3>
              &hellip;or how about something else? <Icon i="search" s="h3" />
            </h3>
            <form action="/search-subjects">
              <input
                type="search"
                size="40"
                placeholder="example: Music"
                name="q"
              />
              <button type="submit">
                <Icon i="search" /> Search
              </button>
            </form>
          </div>
        </section>
      ) : (
        <section className="ta-c">
          <h2>
            Let&apos;s get you some subjects! <Icon i="search" s="h2" />
          </h2>
          {/* TODO If the user has no subjects, then also list popular subjects here */}
          <form action="/search-subjects">
            <p>
              <input
                type="search"
                size="40"
                placeholder="example: Music"
                autoFocus
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
      )}

      <CardSubjectInfo />

      <Footer role={role} />
    </Layout>
  )
}

DashboardPage.propTypes = {
  hash: string.isRequired,
  role: string,
  name: string,
  subjects: arrayOf(
    shape({
      entityId: string.isRequired,
      name: string.isRequired,
      body: string.isRequired,
    })
  ),
}

DashboardPage.defaultProps = {
  role: 'sg_anonymous',
  name: 'friend',
  subjects: [],
}

/*

<section>
  <h2>You've got some new notices 🔔</h2>
  <ul className="ls-n">
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

*/
/*

<section>
  <h2>Help us build Sagefy 🌳</h2>

  <details>
    <summary><h3 className="d-ib">Add some cards 🃏</h3></summary>
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
      ><h3 className="d-ib">
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
      ><h3 className="d-ib">
        &hellip;or find something else 🕵🏻‍♀️
      </h3></summary
    >
    <form action="/mocks/search">
      <input type="search" size="40" placeholder="example: Music" />
      <button type="submit">🕵🏻‍♀️ Search</button>
    </form>
  </details>
</section>

*/
