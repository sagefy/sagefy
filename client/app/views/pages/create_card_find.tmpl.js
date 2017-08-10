/* eslint-disable no-underscore-dangle */
const {
    div,
    h1,
    h2,
    p,
    ul,
    li,
    a,
    form,
    input,
    button,
} = require('../../modules/tags')
const { cardWizard } = require('./create_shared.fn')
const previewUnitHead = require('../components/preview_unit_head.tmpl')
const icon = require('../components/icon.tmpl')

module.exports = function createCardFind(data) {
    const { searchResults } = data
    const { myRecentUnits } = data.create

    const inputOpts = {
        type: 'text',
        placeholder: 'Search Units',
        name: 'search',
        size: 40,
    }
    inputOpts.value = data.searchQuery || null

    return div(
        { id: 'create', className: 'page create--card-find' },
        h1('Find a Unit to Add Cards'),
        cardWizard('find'),
        myRecentUnits && myRecentUnits.length
            ? div(
                  h2('My Recent Units'),
                  ul(
                      { className: 'create--card-find__my-recents' },
                      myRecentUnits.map(unit =>
                          li(
                              a(
                                  {
                                      href: `/create/card/list?${unit.entity_id}`,
                                      className: 'create--card-find__choose',
                                      dataset: {
                                          id: unit.entity_id,
                                          name: unit.name,
                                      },
                                  },
                                  icon('create'),
                                  ' Choose This Unit'
                              ),
                              previewUnitHead({
                                  name: unit.name,
                                  body: unit.body,
                              })
                          )
                      )
                  ),
                  p({ className: 'create--card-find__or' }, 'or')
              )
            : null,
        h2('Search for a Unit'),
        form(
            { className: 'form--horizontal create--card-find__form' },
            div(
                { className: 'form-field form-field--search' },
                input(inputOpts)
            ),
            button(
                { type: 'submit', className: 'create--card-find__search' },
                icon('search'),
                ' Search'
            )
        ),
        searchResults && searchResults.length
            ? ul(
                  { className: 'create--card-find__results' },
                  searchResults.map(result =>
                      li(
                          a(
                              {
                                  href: `/create/card/list?${result._id}`,
                                  className: 'create--card-find__choose',
                                  dataset: {
                                      id: result._id,
                                      name: result._source.name,
                                  },
                              },
                              icon('create'),
                              ' Choose This Unit'
                          ),
                          previewUnitHead({
                              name: result._source.name,
                              body: result._source.body,
                          })
                      )
                  )
              )
            : p('No results.'),
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
