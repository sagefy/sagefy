import React from 'react'
import { string, shape } from 'prop-types'
import get from 'lodash.get'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'

export default function StatisticsPage({ hash, statistics }) {
  return (
    <Layout
      hash={hash}
      page="StatisticsPage"
      title="Statistics"
      description="View Sagefy's growth on our public statistics page."
    >
      <header className="my-c">
        <p>
          <a href="/">
            Go back <Icon i="home" /> home
          </a>
        </p>
        <h1>Statistics</h1>
      </header>

      <section>
        <table className="ta-r">
          <thead>
            <tr>
              <th>Metric, daily mean</th>
              <th>7 days</th>
              <th>28 days</th>
              <th>364 days</th>
            </tr>
          </thead>
          <tbody>
            {[
              ['Start goal subject', 'userSubject'],
              ['Response ≥99%', 'responsez'],
              ['Response ≥90%', 'responsex'],
              ['Response, all', 'response'],
              ['New subject', 'subject'],
              ['Edit subject', 'subjectUpdate'],
              ['New card', 'card'],
              ['Edit card', 'cardUpdate'],
              ['Post', 'post'],
              ['Topic', 'topic'],
              ['Sign up', 'user'],
              ['Visits', '?'],
              ['Returning visits', '?'],
              ['Pageviews', '?'],
              ['Pageviews / visit', '?'],
            ].map(([name, field]) => (
              <tr key={name}>
                <td>{name}</td>
                <td>
                  <code>{get(statistics, `${field}7`)}</code>
                </td>
                <td>
                  <code>{(get(statistics, `${field}28`) / 28).toFixed(2)}</code>
                </td>
                <td>
                  <code>
                    {(get(statistics, `${field}364`) / 364).toFixed(2)}
                  </code>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
      <section>
        <h2>Most frequent pages by type last 7 days</h2>
        <ul>
          <li>?</li>
        </ul>
      </section>
      <section>
        <h2>Most frequent subjects last 7 days</h2>
        <ul>
          {get(statistics, 'recentPopularSubjects.nodes', []).map(
            ({ entityId, name }) => (
              <li key={`statistics-subject-${entityId}`}>
                <a href={`/subjects/${to58(entityId)}`}>{name}</a>
              </li>
            )
          )}
        </ul>
      </section>
      <section>
        <h2>Most frequent subject searches with no result last 7 days</h2>
        <ul>
          <li>?</li>
        </ul>
      </section>
      <section>
        <h2>Top referral sources last 7 days</h2>
        <ul>
          <li>?</li>
        </ul>
      </section>
      <section>
        <h2>Most frequent Google search keywords last 7 days</h2>
        <ul>
          <li>?</li>
        </ul>
      </section>
      <section>
        <h2>Most frequent operating systems last 7 days</h2>
        <ul>
          <li>?</li>
        </ul>
      </section>
      <section>
        <h2>Most frequent browsers and versions last 7 days</h2>
        <ul>
          <li>?</li>
        </ul>
      </section>
      <section>
        <h2>Most visitor countries last 7 days</h2>
        <ul>
          <li>?</li>
        </ul>
      </section>
    </Layout>
  )
}

StatisticsPage.propTypes = {
  hash: string.isRequired,
  statistics: shape({}).isRequired,
}
