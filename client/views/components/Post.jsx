import React from 'react'
import ReactMarkdown from 'react-markdown'
import TimeAgo from 'timeago-react'
import { shape, string, instanceOf } from 'prop-types'
import { to58 } from 'uuid58'

export default function Post({
  id,
  created,
  userId,
  userByUserId,
  sessionId,
  body,
}) {
  const { name: userName, md5Email } = userByUserId || {}
  return (
    <tr className="Post" id={`post-${to58(id)}`}>
      <td>
        <p>
          {userId ? (
            <a href={`/users/${to58(userId)}`}>
              <img
                src={`https://www.gravatar.com/avatar/${md5Email}?d=mm&amp;s=80`}
                alt="avatar"
              />
            </a>
          ) : (
            <img
              src={`https://www.gravatar.com/avatar/_?d=mm&amp;s=80`}
              alt="avatar"
            />
          )}
        </p>
      </td>
      <td>
        <p>
          {userId ? (
            <a href={`/users/${to58(userId)}`}>{userName}</a>
          ) : (
            <span>
              Ghost <code>{to58(sessionId).slice(0, 6)}</code>
            </span>
          )}{' '}
          <small>
            <TimeAgo datetime={created} />
          </small>
        </p>
        <ReactMarkdown source={body} />
        {/* <small>
              <ul className="ls-i ta-r" style="margin-bottom:1rem">
                <li>
                  <a href="#">↩️ Reply</a
                  >{/*-- if own, edit -/}
                </li>
                <li><a href="#">🥢 Share</a></li>
              </ul>
            </small> */}
      </td>
    </tr>
  )
}

Post.propTypes = {
  id: string.isRequired,
  created: instanceOf(Date).isRequired,
  userId: string,
  userByUserId: shape({}),
  sessionId: string,
  body: string.isRequired,
}

Post.defaultProps = {
  userByUserId: {},
  userId: null,
  sessionId: null,
}
