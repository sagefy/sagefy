const {div, h1, h3, ul, li, a, p, hr} = require('../../modules/tags')
const icon = require('../components/icon.tmpl')
const spinner = require('../components/spinner.tmpl')


const setResult = (set) =>
    [
        a(  // TODO-2 if already in sets, don't show this button
            {
                id: set.entity_id,
                href: '#',
                className: 'add-to-my-sets'
            },
            icon('create'),
            ' Add to My Sets'
        ),
        div(
            h3(set.name),
            p(set.body),
            a(
                {
                    href: `/sets/${set.entity_id}/tree`,
                    className: 'view-units',
                },
                icon('unit'),
                ' View Units'
            )
        )
    ]


module.exports = (data) => {
    if(!data.recommendedSets.length) { return spinner() }
    return div(
        {id: 'recommended-sets', className: 'page'},
        h1('Recommended Sets'),
        ul(
            data.recommendedSets.map(set => li(setResult(set)))
        ),
        hr(),
        a({href: '/search?mode=as_learner'}, icon('search'), ' Search Sets')
    )
}
