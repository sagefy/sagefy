{li, div, img, p, a, i, span, ul, li, h3} = require('../../modules/tags')
{timeAgo, ucfirst} = require('../../modules/auxiliaries')

listOfObjectsToString = (list) ->
    return list.map((member) ->
        Object.keys(member).map((key) ->
            "#{key}: #{member[key]}"
        ).join(', ')
    ).join('; ')

renderProposal = (data) ->
    return unless data.kind is 'proposal'
    evKind = data.entity_version.kind
    ev = data.ev
    return div(
        {className: 'post--proposal'}
        # TODO-2 this is super ugly
        ul(
            li(
                'Status: '
                span(
                    {className: "proposal__status--#{ev.status}"}
                    ucfirst(ev.status)
                )
            )
            li('Kind: ' + ucfirst(evKind))
            li('Name: ' + ev.name)
            li('Language: ' + ev.language)
            li('Body: ' + ev.body) if evKind in ['unit', 'set']
            li('Unit ID: ' + ev.unit_id) if evKind is 'card'
            li('Require IDs: ' + ev.require_ids) if evKind in ['card', 'unit']
            li(
                'Members: ' + listOfObjectsToString(ev.members)
            ) if evKind is 'set'
            # TODO-3 Tags (all)
        )
        renderCardProposal(data) if evKind is 'card'
    )

renderCardProposal = (data) ->
    return ul(
        li('Card Kind: ' + ev.kind)
        li('Video Site: ' + ev.site) if ev.kind is 'video'
        li('Video ID: ' + ev.video_id) if ev.kind is 'video'
        li('Question: ' + ev.body) if ev.kind is 'choice'
        li(
            'Options: ' + listOfObjectsToString(ev.options)
        ) if ev.kind is 'choice'
        li('Order: ' + ev.order) if ev.kind is 'choice'
        li(
            'Max Options to Show: ' + ev.max_options_to_show
        ) if ev.kind is 'choice'
    )

    # TODO-2 diff from previous version

voteResponse = (response) ->
    return unless response?
    return [
        span(
            {
                className: "label--#{if response then 'good' else 'bad'}"
            }
            i({className: "fa fa-thumbs-#{if response then 'up' else 'down'}"})
            if response then ' Yes' else ' No'
        )
        ' '
    ]

module.exports = (data, currentUserID) ->
    {topic_id} = data
    return li(
        {
            id: data.id
            className: 'post'
        }
        div(
            {className: 'post__avatar'}
            a(
                {href: "/users/#{data.user_id}"}
                img(
                    {
                        src: data.user_avatar or ''
                        width: 48
                        height: 48
                        'data-title': 'username'
                    }
                )
            )
        )
        div(
            {className: 'post__content'}
            div({className: 'post__when'}, timeAgo(data.created))
            a(
                {
                    className: 'post__name'
                    href: "/users/#{data.user_id}"
                }
                data.user_name or '???'
            )
            div(
                a(
                    {
                        className: 'post__in-reply'
                        href: "/topics/#{data.topic_id}##{data.replies_to_id}"
                    }
                    i({className: 'fa fa-reply'})
                    ' In Reply'
                ) if data.replies_to_id
                ' ' if data.replies_to_id

                h3('Proposal: ' + data.name) if data.kind is 'proposal'

                voteResponse(data.response)

                data.body
            )
            renderProposal(data) if data.kind is 'proposal'
            div(
                {className: 'post__footer'}
                a(
                    {href: "/topics/#{topic_id}/posts/#{data.id}/update"}
                    i({className: 'fa fa-edit'})
                    ' Edit'
                ) if currentUserID is data.user_id
                a(
                    {href: "/topics/#{topic_id}/posts/create?" +
                           "replies_to_id=#{data.id}"}
                    i({className: 'fa fa-reply'})
                    ' Reply'
                ) if currentUserID isnt data.user_id
                a(
                    {href: "/topics/#{topic_id}/posts/create?" +
                           "replies_to_id=#{data.id}&kind=vote"}
                    i({className: 'fa fa-check'})
                    ' Vote'
                ) if data.kind is 'proposal'
                a(
                    {href: "/topics/#{data.topicID}##{data.id}"}
                    i({className: 'fa fa-share'})
                    ' Share'
                )
                # TODO-3 a(
                #     {href: '#'}
                #     i({className: 'fa fa-flag'})
                #     ' Flag'
                # ) if currentUserID isnt data.user_id
            )
        )
    )
