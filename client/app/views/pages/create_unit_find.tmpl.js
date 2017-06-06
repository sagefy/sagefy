/* eslint-disable no-underscore-dangle */
const { div, h1, h2, p, ul, li, a, form, input, button } =
    require('../../modules/tags')
const { unitWizard } = require('./create_shared.fn')
const previewSubjectHead = require('../components/preview_subject_head.tmpl')
const icon = require('../components/icon.tmpl')

module.exports = function createUnitFind(data) {
    const { searchResults } = data
    const { myRecentSubjects } = data.create

    const inputOpts = {
        type: 'text',
        placeholder: 'Search Subjects',
        name: 'search',
        size: 40
    }
    inputOpts.value = data.searchQuery || null

    return div(
        { id: 'create', className: 'page create--unit-find' },
        h1('Find a Subject to Add Units'),
        unitWizard('find'),

        myRecentSubjects && myRecentSubjects.length ? div(
            h2('My Recent Subjects'),
            ul(
                { className: 'create--unit-find__my-recents' },
                myRecentSubjects.map(subject => li(
                    a(
                        {
                            href: `/create/unit/list?${subject.entity_id}`,
                            className: 'create--unit-find__choose',
                            dataset: {
                                id: subject.entity_id,
                                name: subject.name,
                            },
                        },
                        icon('create'),
                        ' Choose This Subject'
                    ),
                    previewSubjectHead({
                        name: subject.name,
                        body: subject.body,
                    })
                ))
            ),
            p({ className: 'create--unit-find__or' }, 'or')
        ) : null,

        h2('Search for a Subject'),
        form(
            { className: 'form--horizontal create--unit-find__form' },
            div(
                { className: 'form-field form-field--search' },
                input(inputOpts)
            ),
            button(
                { type: 'submit', className: 'create--unit-find__search' },
                icon('search'),
                ' Search'
            )
        ),
        searchResults && searchResults.length ? ul(
            { className: 'create--unit-find__results' },
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
                    ' Choose This Subject'
                ),
                previewSubjectHead({
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
