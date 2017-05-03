/* eslint-disable no-underscore-dangle */
const {div, h1, h2, p, ul, li, a, form, input, button} =
    require('../../modules/tags')
const {unitWizard} = require('./create_shared.fn')
const previewSetHead = require('../components/preview_set_head.tmpl')
const icon = require('../components/icon.tmpl')

module.exports = function createUnitFind(data) {
    const {searchResults} = data
    const {myRecentSets} = data.create

    const inputOpts = {
        type: 'text',
        placeholder: 'Search Sets',
        name: 'search',
        size: 40
    }
    inputOpts.value = data.searchQuery || null

    return div(
        {id: 'create', className: 'page create--unit-find'},
        h1('Find a Set to Add Units'),
        unitWizard('find'),

        myRecentSets && myRecentSets.length ? div(
            h2('My Recent Sets'),
            ul(
                {className: 'create--unit-find__my-recents'},
                myRecentSets.map(set => li(
                    a(
                        {
                            href: `/create/unit/list?${set.entity_id}`,
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
            ),
            p({className: 'create--unit-find__or'}, 'or')
        ) : null,

        h2('Search for a Set'),
        form(
            {className: 'form--horizontal create--unit-find__form'},
            div(
                {className: 'form-field form-field--search'},
                input(inputOpts)
            ),
            button(
                {type: 'submit', className: 'create--unit-find__search'},
                icon('search'),
                ' Search'
            )
        ),
        searchResults && searchResults.length ? ul(
            {className: 'create--unit-find__results'},
            searchResults.map(result => li(
                a(
                    {
                        href: `/create/unit/list?${result._id}`,
                        className: 'create--unit-find__choose',
                        dataset: {
                            id: result._id,
                            name: result._source.name,
                        },
                    },
                    icon('create'),
                    ' Choose This Set'
                ),
                previewSetHead({
                    name: result._source.name,
                    body: result._source.body,
                })
            ))
        ) : p('No results.'),

        a(
            {
                href: '/create',
                className: 'create__home',
            },
            icon('back'),
            ' Return to Create Overview'
        )
    )
}
