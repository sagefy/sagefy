{li, div, img, p, a, i} = require('../../modules/tags')
timeAgo = require('../../modules/auxiliaries').timeAgo

module.exports = (data) ->
    li(
        {
            id: data.id
            className: 'post'
        }
        div(
            {className: 'post__avatar'}
            img(
                {src: data.avatar or '', 'data-title': 'username'}
            )
        )
        div(
            {className: 'post__content'}
            div({className: 'post__when'}, timeAgo(data.when))
            a(
                {
                    className: 'post__name'
                    href: "/users/#{data.userID}"
                }
                data.name
            )
            p(
                a(
                    {href: "/topics/#{data.topicID}##{data.replies_to_id}"}
                    'In Reply'
                )
            ) if data.replies_to_id
            p(data.body)
            div(
                {className: 'post__footer'}
                a(
                    {href: "/posts/#{data.id}/update"}
                    i({className: 'fa fa-edit'})
                    ' Edit'
                )  # if current user
                a(
                    {href: "/posts/create?replies_to_id=#{data.id}"}
                    i({className: 'fa fa-reply'})
                    ' Reply'
                )
                a(
                    {href: "/posts/create?replies_to_id=#{data.id}"}
                    i({className: 'fa fa-vote'})
                    ' Vote'
                )  # if proposal or flag
                a(
                    {href: "/topics/#{data.topicID}##{data.id}"}
                    i({className: 'fa fa-share'})
                    ' Share'
                )
                a(
                    {href: '#'}
                    i({className: 'fa fa-flag'})
                    ' Flag'
                )
            )
        )
    )
