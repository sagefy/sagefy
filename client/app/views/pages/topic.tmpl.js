const capitalize = require('lodash.capitalize')
const { header, h3, hgroup, div, h1, ul, a } = require('../../helpers/tags')
// const c = require('../../helpers/content').get
const post = require('../components/post.tmpl')
const followButton = require('../components/follow_button.tmpl')
const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')
const { getIsLoggedIn } = require('../../selectors/base')

// TODO-2 User doesn't show right after creating a new post in the topic view

const entity = (topic, data) => {
  const entityKind = topic.entity_kind
  const entityID = topic.entity_id
  const entityObj =
    entityKind === 'card'
      ? data.cards[entityID]
      : entityKind === 'unit'
        ? data.units[entityID]
        : entityKind === 'subject' ? data.subjects[entityID] : {}
  const entityName = (entityObj && entityObj.name) || ''
  return h3(`${capitalize(entityKind)}: ${entityName}`)
}

module.exports = data => {
  if (getIsLoggedIn(data) === null) {
    return spinner()
  }

  const id = data.routeArgs[0]
  const posts = data.topicPosts && data.topicPosts[id]
  const topic = data.topics && data.topics[id]

  if (!topic || !posts) {
    return spinner()
  }

  return div(
    { id: 'topic', className: 'page' },
    header(
      followButton('topic', id, data.follows),
      hgroup(
        entity(topic, data),
        h1(topic.name),
        data.currentUserID === topic.user_id
          ? a(
              { href: `/topics/${topic.id}/update` },
              icon('update'),
              ' Update name'
            )
          : null
      )
    ),
    ul(
      { className: 'posts' },
      posts.map(postData => {
        const user = data.users[postData.user_id]
        return post(
          Object.assign({}, postData, {
            user: {
              name: user && user.name,
              avatar: data.userAvatars[postData.user_id],
            },
            entityVersionsFull:
              postData.kind === 'proposal' &&
              postData.entity_versions.map(ev =>
                Object.assign({}, data.topicPostVersions[ev.kind][ev.id], {
                  entityKind: ev.kind,
                })
              ),
          }),
          data.currentUserID
        )
      })
    ),
    // TODO-2 Pagination

    div(
      { className: 'topic__actions' },
      a(
        {
          className: 'topic__create',
          href: `/topics/${id}/posts/create`,
        },
        icon('create'),
        ' Create a new post'
      )
    )
  )
}
