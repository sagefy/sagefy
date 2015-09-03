{li, div, img, p, a, i} = require('../../modules/tags')
timeAgo = require('../../modules/auxiliaries').timeAgo

module.exports = (data) ->
    li(
        {className: 'post'}
        div(
            {className: 'post__avatar'}
            img(
                {src: data.avatar or '', 'data-title': 'username'}
            )
        )
        div(
            {className: 'post__content'}
            div({className: 'post__when'}, timeAgo(data.when))
            div({className: 'post__name'}, data.name)
            p(data.body)
            div(
                {className: 'post__footer'}
                a(
                    {href: '#'}
                    i({className: 'fa fa-edit'})
                    ' Edit'
                )  # if current user
                a(
                    {href: '#'}
                    i({className: 'fa fa-reply'})
                    ' Reply'
                )
                a(
                    {href: '#'}
                    i({className: 'fa fa-vote'})
                    ' Vote'
                )  # if proposal or flag
                a(
                    {href: '#'}
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
