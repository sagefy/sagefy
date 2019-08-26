import React from 'react'
import { string } from 'prop-types'
import Layout from './components/Layout'
import Icon from './components/Icon'

export default function StatisticsPage({ hash }) {
  return (
    <Layout
      hash={hash}
      page="AnalyticsPage"
      title="AnalyticsPage"
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
            <tr>
              <td>Start goal subject</td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
            </tr>
            <tr>
              <td>Response &ge;99%</td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
            </tr>
            <tr>
              <td>Response &ge;90%</td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
            </tr>
            <tr>
              <td>Response, all</td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
            </tr>
            <tr>
              <td>New subject</td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
            </tr>
            <tr>
              <td>Edit subject</td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
            </tr>
            <tr>
              <td>New card</td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
            </tr>
            <tr>
              <td>Edit card</td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
            </tr>
            <tr>
              <td>Post</td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
            </tr>
            <tr>
              <td>Topic</td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
            </tr>
            <tr>
              <td>User</td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
            </tr>
            <tr>
              <td>Visits</td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
            </tr>
            <tr>
              <td>Returning visits</td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
            </tr>
            <tr>
              <td>Pageviews</td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
            </tr>
            <tr>
              <td>Pageviews / visit</td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
              <td>
                <code>?</code>
              </td>
            </tr>
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
          <li>?</li>
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
      {/* TODO OS / browser / geographic */}
    </Layout>
  )
}

StatisticsPage.propTypes = {
  hash: string.isRequired,
}
