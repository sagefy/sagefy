/*

/* eslint-disable no-underscore-dangle /
const {
  div,
  h1,
  a,
  form,
  button,
  input,
  ul,
  li,
  p,
} = require('../../helpers/tags')
const { unitWizard } = require('./create_shared.fn')
const icon = require('../components/icon.tmpl')
const previewUnitHead = require('../components/preview_unit_head.tmpl')
const { getIsLoggedIn } = require('../../selectors/base')
const spinner = require('../components/spinner.tmpl')
const goLogin = require('../../helpers/go_login')

module.exports = function createUnitAdd(data) {
  if (getIsLoggedIn(data) === null) {
    return spinner()
  }

  if (!getIsLoggedIn(data)) {
    return goLogin()
  }

  const { searchResults } = data
  const inputOpts = {
    type: 'text',
    placeholder: 'Search Units',
    name: 'search',
    size: 40,
  }
  inputOpts.value = data.searchQuery || null

  return div(
    { id: 'create', className: 'page' },
    h1('Add an Existing Unit to Subject'),
    unitWizard('list'),
    a({ href: '/create/unit/list' }, icon('back'), ' Back to List of Units'),
    form(
      { className: 'form--horizontal create--unit-add__form' },
      div({ className: 'form-field form-field--search' }, input(inputOpts)),
      button(
        { type: 'submit', className: 'create--unit-add__search' },
        icon('search'),
        ' Search'
      )
    ),
    searchResults && searchResults.length
      ? ul(
          { className: 'create--unit-add__results' },
          searchResults.map(result =>
            li(
              a(
                {
                  href: '/create/unit/list',
                  className: 'create--unit-add__add',
                  dataset: {
                    kind: result._type,
                    id: result._id,
                    version: result._source.id,
                    name: result._source.name,
                    body: result._source.body,
                  },
                },
                icon('create'),
                ' Add to Subject'
              ),
              previewUnitHead({
                name: result._source.name,
                body: result._source.body,
              })
            )
          )
        )
      : p('No results.')
  )
}

*/
