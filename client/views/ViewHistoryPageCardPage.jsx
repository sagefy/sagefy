import React from 'react'
import { string, shape, arrayOf, instanceOf } from 'prop-types'
import ReactMarkdown from 'react-markdown'
import TimeAgo from 'timeago-react'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import Footer from './components/Footer'
import Menu from './components/Menu'
import getMenuItems from '../util/get-menu-items'

export default function ViewHistoryPageCardPage({
  hash,
  role,
  card: { name: cardName, entityId: cardEntityId },
  versions,
}) {
  return (
    <Layout
      hash={hash}
      page="ViewHistoryPageCardPage"
      title={`History of page card: ${cardName}`}
      description={`View the edit history of the Sagefy card "${cardName}.`}
      canonical={`/cards/${to58(cardEntityId)}`}
    >
      <header>
        <div className="my-c">
          <p>
            Page Card History <Icon i="page" />
            <Icon i="card" />
            <Icon i="history" />
          </p>
          <h1>
            History:{' '}
            <a href={`/page-cards/${to58(cardEntityId)}`}>{cardName}</a>
          </h1>
        </div>

        <Menu
          items={getMenuItems('page-cards', to58(cardEntityId))}
          current="History"
        />
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
              data: { body },
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

ViewHistoryPageCardPage.propTypes = {
  hash: string.isRequired,
  role: string,
  card: shape({}).isRequired,
  versions: arrayOf(
    shape({
      created: instanceOf(Date),
    })
  ).isRequired,
}

ViewHistoryPageCardPage.defaultProps = {
  role: 'sg_anonymous',
}
