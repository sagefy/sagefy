const {div, h1, h2, p, ul, li, a} = require('../../modules/tags')
const {unitWizard} = require('./create_shared.fn')
const previewSetHead = require('../components/preview_set_head.tmpl')
const icon = require('../components/icon.tmpl')

module.exports = function createUnitFind(data) {
    const {myRecentSets} = data.create

    return div(
        {id: 'create', className: 'page'},
        h1('Find a Set to Add Units'),
        unitWizard('find'),

        h2('My Recent Sets'),
        myRecentSets && myRecentSets.length ? ul(
            {className: 'create--unit-find__my-recents'},
            myRecentSets.map(set => li(
                a(
                    {
                        href: '/create/unit/list',
                        className: 'create--unit-find__choose',
                        dataset: {
                            id: set.entity_id,
                            name: set.name,
                        },
                    },
                    icon('create'),
                    ' Choose This Set'
                ),
                previewSetHead({
                    name: set.name,
                    body: set.body,
                })
            ))
        ) : null,

        p({className: 'create--unit-find__or'}, 'or'),

        h2('Search for a Set')
        // Search box and buttons
        // List of sets with √ buttons

        // Back to create page
    )
}
