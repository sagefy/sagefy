import React from 'react'
import { string, shape, arrayOf, instanceOf } from 'prop-types'
import ReactMarkdown from 'react-markdown'
import TimeAgo from 'timeago-react'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import Layout from './components/Layout'
import Icon from './components/Icon'
import Footer from './components/Footer'

export default function ViewHistorySubjectPage({
  hash,
  role,
  subject: { entityId: subjectEntityId, name: subjectName },
  versions,
}) {
  return (
    <Layout
      hash={hash}
      page="ViewHistorySubjectPage"
      title={`History of "${subjectName}"`}
      description={`View the editing history of the Sagefy subject "${subjectName}".`}
    >
      <header>
        <div className="my-c">
          <p>
            Subject History <Icon i="subject" />
            <Icon i="history" />
          </p>
          <h1>
            History:{' '}
            <a href={`/subjects/${to58(subjectEntityId)}`}>{subjectName}</a>
          </h1>
        </div>
        <small>
          <ul className="ls-i ta-r">
            {/* <li><a href="/mocks/follows">👂🏿 Follow</a></li> */}
            <li>
              <a href={`/subjects/${to58(subjectEntityId)}/talk`}>
                <Icon i="talk" s="s" /> Talk
              </a>
            </li>
            <li>
              <Icon i="history" s="s" /> History
            </li>
            <li>
              <a href={`/subjects/${to58(subjectEntityId)}/edit`}>
                <Icon i="edit" s="s" /> Edit
              </a>
            </li>
          </ul>
        </small>
        {/* TODO stats section */}
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
              body,
              details,
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
                      {body && (
                        <li>
                          <strong>Body</strong>:{' '}
                          <ReactMarkdown
                            source={body}
                            disallowedTypes={['heading']}
                          />
                        </li>
                      )}
                      {details && (
                        <li>
                          <strong>Details</strong>:{' '}
                          <ReactMarkdown
                            source={details}
                            disallowedTypes={['heading']}
                          />
                        </li>
                      )}
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

ViewHistorySubjectPage.propTypes = {
  hash: string.isRequired,
  role: string,
  subject: shape({
    entityId: string.isRequired,
    name: string.isRequired,
  }).isRequired,
  versions: arrayOf(
    shape({
      created: instanceOf(Date).isRequired,
      status: string.isRequired,
      userByUserId: shape({
        id: string.isRequired,
        name: string.isRequired,
      }),
      sessionId: string,
      name: string.isRequired,
      body: string.isRequired,
      details: string,
    })
  ).isRequired,
}

ViewHistorySubjectPage.defaultProps = {
  role: 'sg_anonymous',
}
