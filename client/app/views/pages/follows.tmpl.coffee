{div, h1, p, a, i, ul, li, strong} = require('../../modules/tags')
c = require('../../modules/content').get
{ucfirst} = require('../../modules/auxiliaries')

module.exports = (data) ->
    return div(
        {id: 'follows', className: 'col-6'}
        h1('Follows')
        a(
            {href: '/notices'}
            i({className: 'fa fa-chevron-left'})
            ' Back to notices.'
        )
        if data.follows \
            then follows(data.follows) \
            else div({className: 'spinner'})
    )

follows = (data) ->
    if not data.length
        return p(
            'No follows. '
            a(
                {href: '/search'},
                i({className: 'fa fa-search'})
                ' Search'
            )
        )
    return ul(follow(f) for f in data)

follow = (data) ->
    return li(
        {className: 'follow'}
        a(
            {
                id: data.id
                href: '#'
                className: 'unfollow button button--bad'
            }
            'Unfollow'
        )
        div(
            strong(ucfirst(data.entity.kind))
            ': '
            data.entity.name
        )
    )
