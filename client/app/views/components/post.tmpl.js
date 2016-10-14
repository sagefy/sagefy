const {li, div, img, a, span, ul, h3} = require('../../modules/tags')
const {timeAgo, ucfirst} = require('../../modules/auxiliaries')
const icon = require('./icon.tmpl')

const listOfObjectsToString = (list = []) =>
    list.map((member) =>
        Object.keys(member).map((key) =>
            `${key}: ${member[key]}`
        ).join(', ')
    ).join('; ')

const renderProposal = (data) => {
    if (!data.kind === 'proposal') { return }
    const evKind = data.entity_version.kind
    const ev = data.ev || {}
    return div(
        {className: 'post__proposal'},
        // TODO-2 this is super ugly
        ul(
            li(
                'Status: ',
                span(
                    {className: `post__proposal-status--${ev.status}`},
                    ucfirst(ev.status)
                )
            ),
            li('Kind: ' + ucfirst(evKind)),
            li('Name: ' + ev.name),
            li('Language: ' + ev.language),
            ['unit', 'set'].indexOf(evKind) > -1 ?
                li('Body: ' + ev.body) :
                null,
            evKind === 'card' ? li('Unit ID: ' + ev.unit_id) : null,
            ['unit', 'set'].indexOf(evKind) > -1 ?
                li('Require IDs: ' + ev.require_ids) :
                null,
            evKind === 'set' ? li(
                'Members: ' + listOfObjectsToString(ev.members)
            ) : null
            // TODO-3 Tags (all)
        ),
        evKind === 'card' ? renderCardProposal(data) : null
    )
}

const renderCardProposal = (data) => {
    const ev = data.ev || {}
    return ul(
        li('Card Kind: ' + ev.kind),
        ev.kind === 'video' ? li('Video Site: ' + ev.site) : null,
        ev.kind === 'video' ? li('Video ID: ' + ev.video_id) : null,
        ev.kind === 'choice' ? li('Question: ' + ev.body) : null,
        ev.kind === 'choice' ? li(
            'Options: ' + listOfObjectsToString(ev.options)
        ) : null,
        ev.kind === 'choice' ? li('Order: ' + ev.order) : null,
        ev.kind === 'choice' ? li(
            'Max Options to Show: ' + ev.max_options_to_show
        ) : null
    )
    // TODO-2 diff from previous version
}

const voteResponse = (response) => {
    if(!response) { return }
    return [
        span(
            {
                className: `post__vote--${response ? 'good' : 'bad'}`
            },
            icon(response ? 'good' : 'bad'),
            response ? ' Yes' : ' No'
        ),
        ' '
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
            {className: 'post__avatar'},
            a(
                {href: `/users/${data.user_id}`},
                img({
                    src: data.user_avatar || '',
                    width: 48,
                    height: 48
                })
            )
        ),
        div(
            {className: 'post__content'},
            div({className: 'post__when'}, timeAgo(data.created)),
            a(
                {
                    className: 'post__name',
                    href: `/users/${data.user_id}`,
                },
                data.user_name || '???'
            ),
            div(
                data.replies_to_id ? a(
                    {
                        className: 'post__in-reply',
                        href: `/topics/${data.topic_id}#${data.replies_to_id}`
                    },
                    icon('reply'),
                    ' In Reply'
                ) : null,
                data.replies_to_id ? ' ' : null,
                data.kind === 'proposal' ? h3('Proposal: ' + data.name) : null,
                voteResponse(data.response),
                data.body
            ),
            data.kind === 'proposal' ? renderProposal(data) : null,
            div(
                {className: 'post__footer'},
                currentUserID === data.user_id ? a(
                    {href: `/topics/${topicId}/posts/${data.id}/update`},
                    icon('update'),
                    ' Edit'
                ) : a(
                    {href: `/topics/${topicId}/posts/create?` +
                           `replies_to_id=${data.id}`},
                    icon('reply'),
                    ' Reply'
                ),
                data.kind === 'proposal' ? a(
                    {href: `/topics/${topicId}/posts/create?` +
                           `replies_to_id=${data.id}&kind=vote`},
                    icon('vote'),
                    ' Vote'
                ) : null,
                a(
                    {href: `/topics/${data.topicID}#${data.id}`},
                    icon('post'),
                    ' Share'
                )
                // TODO-3 a(
                //     {href: '#'}
                //     icon('remove')
                //     ' Flag'
                // ) if currentUserID isnt data.user_id
            )
        )
    )
}
