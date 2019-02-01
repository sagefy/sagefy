import React from 'react'
import Icon from '../components/Icon'
import Footer from '../components/Footer'

export default function SuggestPage() {
  return (
    <div className="SuggestPage">
      <header>
        <h1>
          Suggest new Sagefy subjects <Icon i="suggest" s="xxl" />
        </h1>
        <p>
          Can&apos;t find a free online learning experience for what you want
          to learn?
          <br />
          <em>Request and upvote here!</em> No sign-up or log-in required.
        </p>
      </header>

      {/*
        If the user isn't logged in, ask them to (optionally) sign up to get notified or provide an email address
      */}

      <section>
        <table>
          <tr>
            <td className="text-align-center collapse-margins">
              <p>
                <button type="button" disabled>
                  <Icon i="confirmed" />
                </button>
              </p>
              <pre>
                <small>25 votes</small>
              </pre>
            </td>
            <td className="collapse-margins">
              <h3>Introduction to American Sign Language</h3>
              <p>
                An introduction to fingerspelling, basic greetings, and summary
                statistics about ASL.
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
              <pre>
                <small>12 votes</small>
              </pre>
            </td>
            <td className="collapse-margins">
              <h3>Japanese Art History</h3>
              <p>
                A survey of periods, artists, and works in Japanese art history
              </p>
            </td>
          </tr>
        </table>

        {/* Max 10, paginate */}
      </section>

      <section>
        <h2>
          Make a new suggestion <Icon i="suggest" s="xl" />
        </h2>
        <form>
          <p>
            <label htmlFor="name">Title</label>
            <input type="text" size="40" name="name" id="name" />
          </p>
          <p>
            <label htmlFor="body">
              Description <small>optional</small>
            </label>
            <textarea cols="40" name="body" id="body" />
          </p>
          <p>
            <button type="submit">
              <Icon i="suggest" s="xl" /> Add Suggestion
            </button>
          </p>
        </form>
      </section>

      <Footer />
    </div>
  )
}
