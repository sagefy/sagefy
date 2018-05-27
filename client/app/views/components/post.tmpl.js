const { li, div, img, a, span, h3, hr } = require('../../helpers/tags')
const { timeAgo } = require('../../helpers/auxiliaries')
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
      div({ className: 'post__when' }, timeAgo(data.created)),
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
        ) : null, */
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
