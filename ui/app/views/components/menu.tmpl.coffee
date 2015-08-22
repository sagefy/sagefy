# TODO move copy to content directory
module.exports = (data) ->
    return div(
        {className: 'menu'}
        div(
            {className: 'menu__overlay'}
        )
        a(
            {
                href: '#'
                className: 'menu__trigger'
                'data-title': 'Menu'
            }
            div({className: 'menu__logo'})
            i({className: 'menu__close fa fa-times-circle'})
        )
        ul(
            {className: 'menu__items'}
            menuItem(d) for d in data
        )
    )
