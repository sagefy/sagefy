/*
- name       required, what to send to the API
- count      required, number of options to expect
- url      default: null
- multiple     default: false
- inline     default: false
- showClear    default: false
- showOverlay  default: false 0-6, true 7+
- showSearch   default: false 0-20 and not url, true 21+ or url
- options:
  either options or url are required .. [{value: '', label: ''}]
*/

const c = require('../../modules/content').get
const { ul } = require('../../modules/tags')
const optionTemplate = require('./form_field_select_option.tmpl')

module.exports = data => {
  if (!data.options || data.options.length === 0) {
    return c('no_options')
  }

  const html = []

  html.push(
    ul(
      {
        className: `form-field--select__ul${
          data.inline ? ' form-field--select__ul--inline' : ''
        }`,
      },
      data.options.map(o =>
        optionTemplate({
          name: data.name,
          muliple: data.multiple,
          value: o.value,
          checked: data.value
            ? o.value === data.value
            : o.value === data.default,
          label: o.label,
          disabled: o.disabled,
        })
      )
    )
  )

  // if data.showOverlay
  //   html.push(
  //     div({className: 'select__selected'})
  //     // TODO-3 List options that have already been selected
  //     div({className: 'select__overlay'})
  //   )
  //
  // if data.showClear
  //   html.push(
  //     a(
  //       {className: 'clear', href: '#'}
  //       icon('remove')
  //       c('clear')
  //     )
  //   )
  //
  // if data.showSearch
  //   html.push(
  //     input({type: 'search', name: 'search'})
  //   )

  return html
}
