const {div, h1, p, a, ul, li, strong} = require('../../modules/tags')
// const c = require('../../modules/content').get
const {ucfirst} = require('../../modules/auxiliaries')
// const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')

module.exports = (data) => {
    // TODO-2 update this to look for some status field
    // if(!data.follows) { return spinner() }

    return div(
        {id: 'follows'},
        h1('Follows'),
        a(
            {href: '/notices'},
            icon('back'),
            ' Back to notices.'
        ),
        follows(data.follows)
    )
}

const follows = (data) => {
    if(data.length) { return ul(data.map(f => follow(f))) }
    return p(
        'No follows. ',
        a(
            {href: '/search'},
            icon('search'),
            ' Search'
        )
    )
}

const follow = (data) =>
    li(
        {className: 'follow'},
        a(
            {
                id: data.id,
                href: '#',
                className: 'follows__unfollow-button',
            },
            icon('remove'),
            ' Unfollow'
        ),
        div(
            strong(ucfirst(data.entity.kind)),
            ': ',
            data.entity.name
        )
    )
