import React from 'react'
import TimeAgo from 'timeago-react'
import { shape, string, instanceOf } from 'prop-types'
import { to58 } from 'uuid58'
import Post from './Post'
import Icon from './Icon'
import FormErrorsTop from './FormErrorsTop'
import FormErrorsField from './FormErrorsField'

export default function Topic({
  id,
  created,
  name,
  postsByTopicId,
  gqlErrors,
  query,
  body,
}) {
  const selected = query['topic-id'] === to58(id)
  return (
    <li className="Topic" id={`topic-${to58(id)}`}>
      <details open={selected}>
        <summary>
          <h3 className="d-ib">{name}</h3> {/* if author, edit name */}
          <small>
            <TimeAgo datetime={created} />
          </small>
        </summary>
        {postsByTopicId.nodes.length ? (
          <table>
            {postsByTopicId.nodes.map(post => (
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
  postsByTopicId: shape({}),
  gqlErrors: shape({}),
  query: shape({}),
  body: shape({}),
}

Topic.defaultProps = {
  postsByTopicId: { nodes: [] },
  gqlErrors: {},
  query: {},
  body: {},
}
