import React from 'react'
import { string, shape, arrayOf, instanceOf } from 'prop-types'
import TimeAgo from 'timeago-react'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import Footer from './components/Footer'
import Menu from './components/Menu'
import getMenuItems from '../util/get-menu-items'

export default function ViewHistoryUnscoredEmbedCardPage({
  hash,
  role,
  card: { name: cardName, entityId: cardEntityId },
  versions,
}) {
  return (
    <Layout
      hash={hash}
      page="ViewHistoryUnscoredEmbedCardPage"
      title={`History of unscored embed card: ${cardName}`}
      description={`View the edit history of the Sagefy card "${cardName}".`}
    >
      <header>
        <div className="my-c">
          <p>
            Embed Card History <Icon i="embed" />
            <Icon i="card" />
            <Icon i="history" />
          </p>
          <h1>
            History:{' '}
            <a href={`/unscored-embed-cards/${to58(cardEntityId)}`}>
              {cardName}
            </a>
          </h1>
        </div>

        <Menu
          items={getMenuItems('unscored-embed-cards', to58(cardEntityId))}
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
              data: { url },
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
                        {' '}
                        <iframe
                          src={url}
                          width="600"
                          height="400"
                          title={cardName}
                        />
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

ViewHistoryUnscoredEmbedCardPage.propTypes = {
  hash: string.isRequired,
  role: string,
  card: shape({}).isRequired,
  versions: arrayOf(
    shape({
      created: instanceOf(Date),
    })
  ).isRequired,
}

ViewHistoryUnscoredEmbedCardPage.defaultProps = {
  role: 'sg_anonymous',
}
