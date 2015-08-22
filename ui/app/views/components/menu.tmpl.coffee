# TODO move copy to content directory
{nav, div, a, i, ul} = require('../../modules/tags')
menuItem = require('./menu_item.tmpl')
module.exports = (data) ->
    return nav(
        {className: if data.open then 'menu selected' else 'menu'}
        [
            div(
                {className: 'menu__overlay'}
            ) if data.open
            a(
                {
                    href: '#'
                    className: 'menu__trigger'
                    'data-title': 'Menu'
                }
                div({className: 'menu__logo'})
                i({className: 'menu__close fa fa-times-circle'}) if data.open
            )
            ul(
                {className: 'menu__items'}
                menuItem(d) for d in data.items
            ) if data.open
        ]
    )
