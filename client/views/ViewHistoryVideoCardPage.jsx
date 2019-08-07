/* eslint-disable camelcase */
import React from 'react'
import { string, shape, arrayOf, instanceOf } from 'prop-types'
import TimeAgo from 'timeago-react'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import Footer from './components/Footer'

function getVideoUrl(site, video_id) {
  if (site === 'youtube')
    return `https://www.youtube.com/embed/${video_id}?autoplay=1&amp;modestbranding=1&amp;rel=0`
  if (site === 'vimeo') return `https://player.vimeo.com/video/${video_id}`
  return 'https://example.com'
}

export default function ViewHistoryVideoCardPage({
  hash,
  role,
  card: { name: cardName, entityId: cardEntityId },
  versions,
}) {
  return (
    <Layout
      hash={hash}
      page="ViewHistoryVideoCardPage"
      title={`History of video card: ${cardName}`}
      description={`View the edit history of the Sagefy card "${cardName}.`}
    >
      <header>
        <div className="my-c">
          <p>
            Video Card History <Icon i="video" />
            <Icon i="card" />
            <Icon i="history" />
          </p>
          <h1>
            History:{' '}
            <a href={`/video-cards/${to58(cardEntityId)}`}>{cardName}</a>
          </h1>
        </div>

        <small>
          <ul className="ls-i ta-r">
            <li>
              <a href={`/video-cards/${to58(cardEntityId)}/talk`}>
                <Icon i="talk" s="s" /> Talk
              </a>
            </li>
            <li>
              <Icon i="history" s="s" /> History
            </li>
            <li>
              <a href={`/video-cards/${to58(cardEntityId)}/edit`}>
                <Icon i="edit" s="s" /> Edit
              </a>
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
              data: { site, video_id },
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
                        <iframe
                          src={getVideoUrl(site, video_id)}
                          width="600"
                          height="400"
                          allowFullScreen="true"
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

ViewHistoryVideoCardPage.propTypes = {
  hash: string.isRequired,
  role: string,
  card: shape({}).isRequired,
  versions: arrayOf(
    shape({
      created: instanceOf(Date),
    })
  ).isRequired,
}

ViewHistoryVideoCardPage.defaultProps = {
  role: 'sg_anonymous',
}
