/*

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

module.exports = (store, broker) => {
  broker.add({
    'click #topic .follow'(e) {
      if (e) e.preventDefault()
      // TODO-2 el
    },

    'click #topic .unfollow'(e) {
      if (e) e.preventDefault()
      // TODO-2 el
    },

    'click #topic .load-more'(e) {
      if (e) e.preventDefault()
      // TODO-2 el
    },
  })
}




const { li, div, img, a, span, h3, hr } = require('../../helpers/tags')
const timeago = require('./timeago.tmpl')
const icon = require('./icon.tmpl')
const previewCard = require('./preview_card.tmpl')
const previewUnit = require('./preview_unit.tmpl')
const previewSubject = require('./preview_subject.tmpl')

const renderProposal = data => {
  if (!data.kind === 'proposal') {
    return null
  }
  const entityVersions = data.entityVersionsFull || []
  return div(
    { className: 'post__proposal' },
    entityVersions.map(version => {
      const { entityKind } = version
      if (entityKind === 'card') {
        return [
          previewCard(
            Object.assign({}, version, {
              unit: { name: version.unit_id },
              requires:
                version.require_ids && version.require_ids.map(id => ({ id })),
            })
          ),
          hr(),
        ]
      }
      if (entityKind === 'unit') {
        return [
          previewUnit(
            Object.assign({}, version, {
              requires:
                version.require_ids && version.require_ids.map(id => ({ id })),
            })
          ),
          hr(),
        ]
      }
      if (entityKind === 'subject') {
        return [previewSubject(version), hr()]
      }
      return null
    })
  )
}

const voteResponse = response => {
  if (!response) {
    return null
  }
  return [
    span(
      {
        className: `post__vote--${response ? 'good' : 'bad'}`,
      },
      icon(response ? 'good' : 'bad'),
      response ? ' Yes' : ' No'
    ),
    ' ',
  ]
}

module.exports = (data, currentUserID) => {
  const topicId = data.topic_id
  return li(
    {
      id: data.id,
      className: 'post',
    },
    div(
      { className: 'post__avatar' },
      a(
        { href: `/users/${data.user_id}` },
        img({
          src: data.user.avatar || '',
          width: 48,
          height: 48,
        })
      )
    ),
    div(
      { className: 'post__content' },
      div({ className: 'post__when' }, timeago(data.created)),
      a(
        {
          className: 'post__name',
          href: `/users/${data.user_id}`,
        },
        data.user.name || '???'
      ),
      div(
        data.replies_to_id
          ? a(
              {
                className: 'post__in-reply',
                href: `/topics/${data.topic_id}#${data.replies_to_id}`,
              },
              icon('reply'),
              ' In Reply'
            )
          : null,
        data.replies_to_id ? ' ' : null,
        data.kind === 'proposal' ? h3('Proposal') : null,
        voteResponse(data.response),
        data.body
      ),
      data.kind === 'proposal' ? renderProposal(data) : null,
      div(
        { className: 'post__footer' },
        currentUserID === data.user_id
          ? a(
              {
                href: `/topics/${topicId}/posts/${data.id}/update`,
              },
              icon('update'),
              ' Edit'
            )
          : a(
              {
                href:
                  `/topics/${topicId}/posts/create?` +
                  `replies_to_id=${data.id}`,
              },
              icon('reply'),
              ' Reply'
            ),
        /* PP@ data.kind === 'proposal' ? a(
          {href: `/topics/${topicId}/posts/create?` +
               `replies_to_id=${data.id}&kind=vote`},
          icon('vote'),
          ' Vote'
        ) : null, *\/
        data.kind === 'proposal'
          ? a({ href: '/create' }, icon('create'), ' Create Another Proposal')
          : null,
        a(
          { href: `/topics/${data.topicID}#${data.id}` },
          icon('post'),
          ' Share'
        )
        // TODO-3 a(
        //   {href: '#'}
        //   icon('remove')
        //   ' Flag'
        // ) if currentUserID isnt data.user_id
      )
    )
  )
}



module.exports = (store, broker) => {
  broker.add({
    'click .post .expand'(e) {
      if (e) {
        e.preventDefault()
      }
      // TODO-2 el
    },
  })
}

*/
