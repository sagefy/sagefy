{li, a, i, div} = require('../../modules/tags')

module.exports = (data) ->
    return li(
        {className: 'menu__item'}
        a(
            {href: data.url}
            [
                i({className: "fa fa-#{data.icon}"})
                div(
                    {className: 'menu__item__title'}
                    data.title
                )
            ]
        )
    )
