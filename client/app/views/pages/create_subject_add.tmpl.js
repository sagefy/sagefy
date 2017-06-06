/* eslint-disable no-underscore-dangle */

const { div, h1, form, input, button, a, ul, li, p } =
    require('../../modules/tags')
const icon = require('../components/icon.tmpl')
const previewUnitHead = require('../components/preview_unit_head.tmpl')
const previewSubjectHead = require('../components/preview_subject_head.tmpl')

module.exports = function createSubjectAdd(data) {
    const { searchResults } = data
    const inputOpts = {
        type: 'text',
        placeholder: 'Search Unit and Subjects',
        name: 'search',
        size: 40
    }
    inputOpts.value = data.searchQuery || null

    return div(
        { id: 'create', className: 'page create--subject-add' },
        h1('Add an Existing Unit or Subject to New Subject'),
        a(
            { href: '/create/subject/create' },
            icon('back'),
            ' Back to Create Subject form'
        ),
        form(
            { className: 'form--horizontal create--subject-add__form' },
            div(
                { className: 'form-field form-field--search' },
                input(inputOpts)
            ),
            button(
                { type: 'submit', className: 'create--subject-add__search' },
                icon('search'),
                ' Search'
            )
        ),
        searchResults && searchResults.length ? ul(
            { className: 'create--subject-add__results' },
            searchResults.map(result => li(
                a(
                    {
                        href: '/create/subject/create',
                        className: 'create--subject-add__add',
                        dataset: {
                            kind: result._type,
                            id: result._id,
                            name: result._source.name,
                            body: result._source.body,
                        },
                    },
                    icon('create'),
                    ' Add to Subject'
                ),
                result._type === 'subject' ?
                    previewSubjectHead({
                        name: result._source.name,
                        body: result._source.body,
                    }) :
                result._type === 'unit' ?
                    previewUnitHead({
                        name: result._source.name,
                        body: result._source.body,
                    }) :
                    null
            ))
        ) : p('No results.')
    )
}
