{li, div, img, p, a, i} = require('../../modules/tags')
timeAgo = require('../../modules/auxiliaries').timeAgo

module.exports = (data, currentUserID) ->
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
                data.body
            )
            div(
                {className: 'post__footer'}
                a(
                    {href: "/posts/#{data.id}/update"}
                    i({className: 'fa fa-edit'})
                    ' Edit'
                ) if currentUserID is data.user_id
                a(
                    {href: "/posts/create?replies_to_id=#{data.id}"}
                    i({className: 'fa fa-reply'})
                    ' Reply'
                ) if currentUserID isnt data.user_id
                a(
                    {href: "/posts/create?replies_to_id=#{data.id}&kind=vote"}
                    i({className: 'fa fa-check'})
                    ' Vote'
                ) if data.kind in ['proposal', 'flag']
                a(
                    {href: "/topics/#{data.topicID}##{data.id}"}
                    i({className: 'fa fa-share'})
                    ' Share'
                )
                a(
                    {href: "/posts/create?replies_to_id=#{data.id}&kind=flag"}
                    i({className: 'fa fa-flag'})
                    ' Flag'
                ) if currentUserID isnt data.user_id
            )
        )
    )
