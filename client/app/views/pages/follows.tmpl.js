const { div, h1, p, a, ul, li } = require('../../modules/tags')
// const c = require('../../modules/content').get
// const spinner = require('../components/spinner.tmpl')
const icon = require('../components/icon.tmpl')
const { copy } = require('../../modules/utilities')
const previewSubjectHead = require('../components/preview_subject_head.tmpl')
const previewUnitHead = require('../components/preview_unit_head.tmpl')
const previewCardHead = require('../components/preview_card_head.tmpl')

module.exports = (data) => {
    // TODO-2 update this to look for some status field
    // if(!data.follows) { return spinner() }

    return div(
        { id: 'follows', className: 'page' },
        h1('Follows'),
        a({ href: '/notices' }, icon('back'), ' Back to notices.'),
        follows(
            data.follows.map((follow) => {
                const ofKinds = data[`${follow.entity.kind}s`] || {}
                const entity = ofKinds[follow.entity.id]
                follow = copy(follow)
                follow.entityFull = entity || {}
                return follow
            })
        )
    )
}

const follows = (data) => {
    if (data.length) {
        return ul(data.map(f => follow(f)))
    }
    return p('No follows. ', a({ href: '/search' }, icon('search'), ' Search'))
}

const follow = (data) => {
    const { kind } = data.entity
    const { name, body } = data.entityFull
    return li(
        { className: 'follow' },
        a(
            {
                id: data.id,
                href: '#',
                className: 'follows__unfollow-button',
            },
            icon('remove'),
            ' Unfollow'
        ),
        kind === 'unit'
            ? previewUnitHead({ name, body, labelKind: true })
            : kind === 'subject'
              ? previewSubjectHead({ name, body, labelKind: true })
              : kind === 'card'
                ? previewCardHead({
                    name,
                    kind: data.entityFull.kind,
                    labelKind: true,
                })
                : kind === 'topic' ? 'A topic' : null
    )
}
