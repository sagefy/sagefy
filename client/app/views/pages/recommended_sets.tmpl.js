const {div, h1, ul, li, a, p, strong, hr} = require('../../modules/tags')
const icon = require('../components/icon.tmpl')
const spinner = require('../components/spinner.tmpl')


// TODO-2 merge with function in `search.tmpl`
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
        strong(icon('set'), ' Set'),
        ': ',
        a(
            {href: `/sets/${set.entity_id}`},
            set.name
        ),
        p(set.body),
        a(
            {
                href: `/sets/${set.entity_id}/tree`,
                className: 'view-units',
            },
            icon('unit'),
            ' View Units'
        )
    ]


module.exports = (data) => {
    if(!data.recommendedSets) { return spinner() }
    return div(
        {id: 'recommended-sets'},
        h1('Recommended Sets'),
        ul(
            data.recommendedSets.map(set => li(setResult(set)))
        ),
        hr(),
        a({href: '/search?mode=as_learner'}, icon('search'), ' Search Sets')
    )
}
