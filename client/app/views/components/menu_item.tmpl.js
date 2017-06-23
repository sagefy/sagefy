const { li, a, div } = require('../../modules/tags')
const icon = require('./icon.tmpl')

module.exports = data =>
    li(
        { className: 'menu__item' },
        a(
            { href: data.url },
            [
                icon(data.icon),
                div(
                    { className: 'menu__item__title' },
                    data.title
                ),
            ]
        )
    )
