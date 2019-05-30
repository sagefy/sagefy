import React from 'react'
import { Link } from 'react-router-dom'
import { shape, string, instanceOf, arrayOf } from 'prop-types'
import { convertUuidToUuid58 as to58 } from 'uuid58'
import ReactMarkdown from 'react-markdown'
import TimeAgo from 'timeago-react'
import Layout from '../components/Layout'
import Icon from '../components/Icon'
import FormErrorsTop from '../components/FormErrorsTop'
import FormErrorsField from '../components/FormErrorsField'
import Footer from '../components/Footer'

function clientizeKind(s) {
  return s.toLowerCase().replace(/_/g, '-')
}

function Post({ id, created, userId, userByUserId, sessionId, body }) {
  const { name: userName, md5Email } = userByUserId || {}
  return (
    <tr id={`post-${to58(id)}`}>
      <td>
        <p>
          {userId ? (
            <Link to={`/users/${to58(userId)}`}>
              <img
                src={`https://www.gravatar.com/avatar/${md5Email}?d=mm&amp;s=80`}
                alt="avatar"
              />
            </Link>
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
            <Link to={`/users/${to58(userId)}`}>{userName}</Link>
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

function Topic({ id, created, name, posts, gqlErrors, query, body }) {
  const selected = query['topic-id'] === to58(id)
  return (
    <li id={`topic-${to58(id)}`}>
      <details open={selected}>
        <summary>
          <h3 className="d-ib">{name}</h3> {/* if author, edit name */}
          <small>
            <TimeAgo datetime={created} />
          </small>
        </summary>
        {posts.nodes.length ? (
          <table>
            {posts.nodes.map(post => (
              <Post {...post} />
            ))}
          </table>
        ) : (
          <p>
            <em>There&apos;s no posts yet. Be the first!</em>
          </p>
        )}
        <form
          id={`create-post-${to58(id)}`}
          method="POST"
          action={`talk/${to58(id)}/post`}
          className="d-ib mx-a"
        >
          <h3>
            Create post <Icon i="post" s="s3" />
          </h3>
          {selected && <FormErrorsTop formErrors={gqlErrors} />}
          {selected && <FormErrorsField formErrors={gqlErrors} field="all" />}
          <input type="hidden" name="topicId" value={id} />
          <p>
            <label htmlFor="body">What do you want to say?</label>
            <textarea
              value={selected ? body.body : null}
              placeholder="example: Should we add more cards?"
              cols="40"
              rows="4"
              id="body"
              name="body"
              required
            />
          </p>
          {selected && <FormErrorsField formErrors={gqlErrors} field="body" />}
          <button type="submit">
            <Icon i="post" /> Write post
          </button>
        </form>
      </details>
    </li>
  )
}

Topic.propTypes = {
  id: string.isRequired,
  created: instanceOf(Date).isRequired,
  name: string.isRequired,
  posts: shape({}),
  gqlErrors: shape({}),
  query: shape({}),
  body: shape({}),
}

Topic.defaultProps = {
  posts: { nodes: [] },
  gqlErrors: {},
  query: {},
  body: {},
}

export default function TalkPage({
  hash,
  role,
  body,
  query,
  gqlErrors,
  entity: { entityId, name: entityName, kind: cardKind },
  topics,
}) {
  const entityKind = cardKind ? 'CARD' : 'SUBJECT'
  return (
    <Layout hash={hash} page="TalkPage" title="Talk" description="-">
      <header>
        <div className="my-c">
          <p>
            {cardKind ? 'Card' : 'Subject'}{' '}
            <Icon i={cardKind ? 'card' : 'subject'} />
          </p>
          <h1>
            Talk:{' '}
            <Link
              to={
                cardKind
                  ? `/${clientizeKind(cardKind)}-cards/${to58(entityId)}`
                  : `/subjects/${to58(entityId)}`
              }
            >
              {entityName}
            </Link>{' '}
            <Icon i="talk" s="h1" />
          </h1>
        </div>
        <small>
          <ul className="ls-i ta-r">
            {/* <li><a href="/mocks/follows">👂🏿 Follow</a></li> */}
            <li>
              <Icon i="talk" s="s" /> Talk
            </li>
            {/* <li><a href="/mocks/history">🎢 History</a></li> */}
            {/* <li><a href="/mocks/update-subject">🌳 Edit</a></li> */}
          </ul>
        </small>
      </header>

      <section>
        {!!topics.length && (
          <h2>
            Topics on <q>{entityName}</q> <Icon i="topic" s="h2" />
          </h2>
        )}
        <ul className="ls-n">
          {topics.map(topic => (
            <Topic {...topic} gqlErrors={gqlErrors} body={body} query={query} />
          ))}
        </ul>
      </section>

      <section className="ta-c my-c">
        <p>
          {topics.length ? (
            <em>Don&apos;t see what you want to talk about?</em>
          ) : (
            <em>There&apos;s no topics yet! Be the first.</em>
          )}
        </p>
        <details id="create-topic-form">
          <summary>
            <h2 className="d-i">
              Create topic <Icon i="topic" s="h2" />{' '}
            </h2>
          </summary>
          <form method="POST" className="ta-l d-ib mx-a">
            <FormErrorsTop formErrors={gqlErrors} />
            <FormErrorsField formErrors={gqlErrors} field="all" />
            <input type="hidden" name="entityId" value={entityId} />
            <input type="hidden" name="entityKind" value={entityKind} />
            <p>
              <label htmlFor="name">What should we call this new topic?</label>
              <input
                type="text"
                value={body.name}
                placeholder="example: Should we add more cards?"
                size="40"
                id="name"
                name="name"
                required
              />
            </p>
            <FormErrorsField formErrors={gqlErrors} field="name" />
            <button type="submit">
              <Icon i="topic" /> Create topic
            </button>
          </form>
        </details>
      </section>
      <Footer role={role} />
    </Layout>
  )
}

TalkPage.propTypes = {
  hash: string.isRequired,
  role: string.isRequired,
  body: shape({}),
  query: shape({}),
  gqlErrors: shape({}),
  entity: shape({ entityId: string, name: string, kind: string }).isRequired,
  topics: arrayOf(shape({})),
}

TalkPage.defaultProps = {
  gqlErrors: {},
  body: {},
  query: {},
  topics: [],
}
