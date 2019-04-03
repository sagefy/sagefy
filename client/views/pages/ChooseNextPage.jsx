import React from 'react'
import { Link } from 'react-router-dom'
import Icon from '../components/Icon'
// TODO import ReactMarkdown from 'react-markdown'

export default function ChooseNextPage() {
  return (
    <div className="ChooseNextPage">
      <section className="m-yc">
        <p>
          <em>
            Right, so <strong>An Introduction to Electronic Music</strong>...
          </em>
        </p>
        <h1>
          Where should we start? <Icon i="subject" s="xxl" />
        </h1>
        {/*
    Alt: Great job with "Complex Waves" 🎉 What's should we focus on next?
  */}
      </section>

      {/* If no child subjects and cards empty... we're done. 🎉 */}
      {/* If only one child subject... just display the info, and button to continue */}
      <section>
        <table>
          <tr>
            <td>
              <p>
                <button type="submit">
                  <Icon i="select" />
                </button>
              </p>
            </td>
            <td className="m-yc">
              <h3>
                <mark>
                  <Link to="/learn-video/2">Complex Waves</Link>
                </mark>
              </h3>
              <p>Describe the composition of complex sounds.</p>
            </td>
          </tr>
          <tr>
            <td>
              <p>
                <button type="button">
                  <Icon i="select" />
                </button>
              </p>
            </td>
            <td className="m-yc">
              <h3>
                <Link to="/learn-video/1">Modulation</Link>
              </h3>
              <p>Describe modulation of sound signals.</p>
            </td>
          </tr>
          <tr>
            <td>
              <p>
                <button type="button">
                  <Icon i="select" />
                </button>
              </p>
            </td>
            <td className="m-yc">
              <h3>
                <Link to="/learn-video/3">Human Hearing</Link>
              </h3>
              <p>
                Describe common properties of human hearing, as hearing pertains
                to electronic music.
              </p>
            </td>
          </tr>
        </table>

        <p className="ta-r">
          <small>(15% learned)</small>
        </p>
      </section>

      <section>
        <p className="ta-r">
          <small>
            <em>Or...</em> on second thought, let&apos;s go to the{' '}
            <Link to="/dashboard">
              <Icon i="dashboard" /> Dashboard
            </Link>
            .
          </small>
        </p>
      </section>
    </div>
  )
}
