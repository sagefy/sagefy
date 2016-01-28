{li, a, i, div} = require('../../modules/tags')
icon = require('./icon.tmpl')

module.exports = (data) ->
    return li(
        {className: 'menu__item'}
        a(
            {href: data.url}
            [
                icon(data.icon)
                div(
                    {className: 'menu__item__title'}
                    data.title
                )
            ]
        )
    )
