import React from 'react'
import { string, shape, arrayOf, instanceOf } from 'prop-types'
import ReactMarkdown from 'react-markdown'
import TimeAgo from 'timeago-react'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import Footer from './components/Footer'

export default function ChoiceCardHistoryPage({
  hash,
  role,
  card: { name: cardName, entityId: cardEntityId },
  versions,
}) {
  return (
    <Layout
      hash={hash}
      page="ChoiceCardHistoryPage"
      title={`History of choice card: ${cardName}`}
      description={`View the edit history of the Sagefy card "${cardName}.`}
    >
      <header>
        <div className="my-c">
          <p>
            Choice Card History <Icon i="choice" />
            <Icon i="card" />
            <Icon i="history" />
          </p>
          <h1>
            History:{' '}
            <a href={`/choice-cards/${to58(cardEntityId)}`}>{cardName}</a>
          </h1>
        </div>

        <small>
          <ul className="ls-i ta-r">
            <li>
              <a href={`/choice-cards/${to58(cardEntityId)}/talk`}>
                <Icon i="talk" s="s" /> Talk
              </a>
            </li>
            <li>
              <Icon i="history" s="s" /> History
            </li>
          </ul>
        </small>
      </header>

      <table>
        <tbody>
          {versions.map(
            ({
              created,
              status,
              userByUserId,
              sessionId,
              name,
              data: { body, options },
            }) => {
              const { id: userId, name: userName } = userByUserId || {}
              return (
                <tr>
                  <td>
                    <ul className="ls-n">
                      <li>
                        <small>{status}</small>
                      </li>
                      <li>
                        <TimeAgo datetime={created} />
                      </li>
                      <li>
                        {userName && (
                          <a href={`/users/${userId}`}>{userName}</a>
                        )}
                        {sessionId && (
                          <span>
                            Ghost <code>{to58(sessionId).slice(0, 6)}</code>
                          </span>
                        )}
                      </li>
                    </ul>
                  </td>
                  <td>
                    <ul className="ls-n">
                      <li>
                        <strong>Name</strong>: {name}
                      </li>
                      <li>
                        <ReactMarkdown source={body} />
                      </li>
                      <li>
                        <ul>
                          {Object.entries(options).map(
                            ([key, { value, correct, feedback }]) => (
                              <li key={key}>
                                {value}
                                <br />
                                <mark className={correct ? 'good' : ''}>
                                  {correct ? (
                                    <Icon i="check" />
                                  ) : (
                                    <Icon i="error" />
                                  )}{' '}
                                  {feedback}
                                </mark>
                              </li>
                            )
                          )}
                        </ul>
                      </li>
                    </ul>
                  </td>
                </tr>
              )
            }
          )}
        </tbody>
      </table>
      <Footer role={role} />
    </Layout>
  )
}

ChoiceCardHistoryPage.propTypes = {
  hash: string.isRequired,
  role: string,
  card: shape({}).isRequired,
  versions: arrayOf(
    shape({
      created: instanceOf(Date),
    })
  ).isRequired,
}

ChoiceCardHistoryPage.defaultProps = {
  role: 'sg_anonymous',
}
