{li, div, img, p, a, i, span} = require('../../modules/tags')
timeAgo = require('../../modules/auxiliaries').timeAgo


# TODO@ proposal fields
# Entity Kind (all)
# Entity ID (all, not on create entity)
# Entity Name (all)
# Entity Language (en only option)
# Entity Body (unit or set)
# Unit Belongs To (card only, should be provided by qs)
# Tags (all)
# Requires (card or unit)
# Members [id, kind] (set)
# Card Kind (card)
# Video Site (video card)
# Video ID (video card)
# Choice Question [Body] (choice card)
# Choice Options [value, correct, feedback] (choice card)
# Choice Feedback (choice card)
# Choice Order (choice card)
# Choice Max Options to Show (choice card)
# TODO diff from previous version

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

                voteResponse(data.response)

                data.body
            )
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
                # TODO a(
                #     {href: '#'}
                #     i({className: 'fa fa-flag'})
                #     ' Flag'
                # ) if currentUserID isnt data.user_id
            )
        )
    )
