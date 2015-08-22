# TODO move copy to content directory
{nav, div, a, i, ul} = require('../../modules/tags')
module.exports = (data) ->
    return nav(
        {className: 'menu'}
        [
            div(
                {className: 'menu__overlay'}
            )
            a(
                {
                    href: '#'
                    className: 'menu__trigger'
                    'data-title': 'Menu'
                }
                [
                    div({className: 'menu__logo'})
                    i({className: 'menu__close fa fa-times-circle'})
                ]
            )
            ul(
                {className: 'menu__items'}
                menuItem(d) for d in data
            )
        ]
    )
