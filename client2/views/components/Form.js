/*


const { form, ul } = require('../../helpers/tags')
const formField = require('./form_field.tmpl')
const formError = require('./form_error.tmpl')

module.exports = ({ fields, errors }) =>
  form(
    fields.map(field => formField(field)),
    errors && errors.length
      ? ul({ className: 'form__errors' }, errors.map(error => formError(error)))
      : null
  )





const { li } = require('../../helpers/tags')
const icon = require('./icon.tmpl')

module.exports = ({ name, message }) =>
  li(
    { className: 'form__error' },
    icon('bad'),
    [' ', name ? `${name}: ` : '', message].join('')
  )

const { div, p, span } = require('../../helpers/tags')
const icon = require('./icon.tmpl')

const kindTmpl = {}
kindTmpl.label = require('./form_field_label.tmpl')
kindTmpl.input = require('./form_field_input.tmpl')
kindTmpl.textarea = require('./form_field_textarea.tmpl')
kindTmpl.button = require('./form_field_button.tmpl')
kindTmpl.select = require('./form_field_select.tmpl')
kindTmpl.list = require('./form_field_list.tmpl')
kindTmpl.entities = require('./form_field_entities.tmpl')

const m = data => {
  const nodes = []
  if (data.label && ['button', 'submit'].indexOf(data.type) === -1) {
    nodes.push(kindTmpl.label(data))
  }
  const fieldTmpl = {
    text: kindTmpl.input,
    email: kindTmpl.input,
    number: kindTmpl.input,
    password: kindTmpl.input,
    hidden: kindTmpl.input,
    textarea: kindTmpl.textarea,
    submit: kindTmpl.button,
    button: kindTmpl.button,
    select: kindTmpl.select,
    list: kindTmpl.list,
    entities: kindTmpl.entities,
  }[data.type]
  if (fieldTmpl) {
    nodes.push(fieldTmpl(data))
  }
  if (data.error) {
    nodes.push(
      span({ className: 'form-field__feedback' }, icon('bad'), data.error)
    )
  }
  if (data.description) {
    nodes.push(p({ className: 'form-field__description' }, data.description))
  }
  return nodes
}

module.exports = data => {
  const classes = [
    'form-field',
    `form-field--${data.type}`,
    `form-field--${data.name}`,
    data.error ? 'form-field--bad' : '',
    data.good ? 'form-field--good' : '',
  ].join(' ')
  return div({ className: classes }, m(data))
}





const { button } = require('../../helpers/tags')
const icon = require('./icon.tmpl')

module.exports = data =>
  button(
    {
      type: 'submit',
      disabled: data.disabled,
      id: data.id,
    },
    icon(data.icon),
    ' ',
    data.label
  )






const { div, ul, li, a, input } = require('../../helpers/tags')
const icon = require('./icon.tmpl')
const previewCardHead = require('./preview_card_head.tmpl')
const previewUnitHead = require('./preview_unit_head.tmpl')
const previewSubjectHead = require('./preview_subject_head.tmpl')

module.exports = data => {
  const entities = data.value || data.default || []
  return div(
    entities.length
      ? ul(
          { className: 'form-field--entities__ul' },
          entities.map((entity, index) =>
            li(
              a(
                {
                  id: entity.id,
                  href: '#',
                  className: 'form-field--entities__remove',
                },
                icon('remove'),
                ' Remove'
              ),
              entity.kind === 'card'
                ? previewCardHead({
                    name: entity.name,
                    kind: entity.kind,
                  })
                : entity.kind === 'unit'
                  ? previewUnitHead({
                      name: entity.name,
                      body: entity.body,
                    })
                  : entity.kind === 'subject'
                    ? previewSubjectHead({
                        name: entity.name,
                        body: entity.body,
                      })
                    : null,
              Object.keys(entity).map(key =>
                input({
                  type: 'hidden',
                  name: `${data.name}.${index}.${key}`,
                  value: entity[key],
                })
              )
            )
          )
        )
      : null,
    data.add
      ? a(
          { className: 'form-field--entities__a', href: data.add.url },
          icon('search'),
          ` ${data.add.label}`
        )
      : null
  )
}






const { input } = require('../../helpers/tags')

module.exports = data =>
  input({
    id: `ff-${data.name}`,
    name: data.name,
    placeholder: data.placeholder || '',
    type: data.type || 'text',
    value: data.value || data.default || '',
    size: data.size || 40,
  })







const c = require('../../helpers/content').get
const { required } = require('../../helpers/validations')
const { label, span } = require('../../helpers/tags')

module.exports = data => {
  const isRequired = data.validations
    ? data.validations.indexOf(required) > -1
    : false
  return label(
    {
      className: 'form-field__label',
      for: `ff-${data.name}`,
    },
    data.label || '',
    data.type === 'message'
      ? null
      : span(
          {
            className: isRequired
              ? 'form-field__required'
              : 'form-field__optional',
          },
          isRequired ? c('required') : c('optional')
        )
  )
}





const capitalize = require('lodash.capitalize')
const {
  table,
  thead,
  tfoot,
  tbody,
  tr,
  th,
  td,
  a,
} = require('../../helpers/tags')
const formFieldInput = require('./form_field_input.tmpl')
const formFieldSelect = require('./form_field_select.tmpl')
const icon = require('./icon.tmpl')

const field = ({ name, index, col, row, lock }) => {
  if (lock) {
    return row[col.name]
  }

  if (col.type === 'select') {
    return formFieldSelect({
      name: `${name}.${index}.${col.name}`,
      value: row[col.name],
      options: col.options,
    })
  }

  if (col.type === 'text') {
    return formFieldInput({
      type: 'text',
      size: 30,
      name: `${name}.${index}.${col.name}`,
      value: row[col.name],
      // TODO-3 placeholder
      // TODO-3 default
    })
  }

  return null
}

module.exports = data => {
  /*
  data.columns: array of field names
  data.values: array of objects
  data.lock [Boolean]
  data.name
  /

  let { value } = data
  if (!value || !value.length) {
    value = [{}]
  }

  const columns = data.columns || []

  return table(
    { 'data-name': data.name },
    thead(
      tr(
        columns.map(col => th({ 'data-col': col.name }, capitalize(col.name))),
        // TODO-2 th()  // For reordering
        th() // For deleting
      )
    ),
    tfoot(
      tr(
        td(
          { colSpan: columns.length + 1 }, // TODO-2 +2 reordering
          a(
            { href: '#', className: 'form-field--list__add-row' },
            icon('create'),
            ' Add Row'
          )
        )
      )
    ),
    tbody(
      value.map((row, index) =>
        tr(
          columns.map(col =>
            td(
              field({
                name: data.name,
                index,
                col,
                row,
                lock: data.lock,
              })
            )
          ),
          // TODO-2 move row td(
          //   a(
          //     {title: 'Reorder', href: '#', className: 'move-row'}
          //     icon('move')
          //   )
          // )
          td(
            a(
              {
                title: 'Remove',
                href: '#',
                className: 'form-field--list__remove-row',
                'data-index': index,
              },
              icon('remove')
            )
          )
        )
      )
    )
  )
}








const closest = require('../../helpers/closest')
const { getFormValues } = require('../../helpers/forms')

module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'click .form-field--list__remove-row'(e, el) {
      if (e) {
        e.preventDefault()
      }
      const form = closest(el, 'form')
      const values = getFormValues(form)
      const table = closest(el, 'table')
      const { name } = table.dataset
      const index = parseInt(el.dataset.index, 10)
      getTasks().removeListFieldRow(values, name, index)
    },

    'click .form-field--list__add-row'(e, el) {
      if (e) {
        e.preventDefault()
      }
      const form = closest(el, 'form')
      const values = getFormValues(form)
      const table = closest(el, 'table')
      const { name } = table.dataset
      const columns = Array.prototype.map
        .call(table.querySelectorAll('th'), xel => xel.dataset.col)
        .filter(c => c)
      getTasks().addListFieldRow(values, name, columns)
    },

    // TODO-3 'dragstart .form-field--list__move-row'(e, el)
    // TODO-3 'drop form-field--list__move-row'(e, el)
  })
}




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
/

const c = require('../../helpers/content').get
const { ul } = require('../../helpers/tags')
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




module.exports = (store, broker) => {
  broker.add({
    'click .select .clear'(e) {
      e.preventDefault()
      // TODO-3 clear options
    },

    // 'change input[type="radio"], input[type="checkbox"]': (e, el) =>
    // TODO-3 update .select__selected to show list of selected names
  })
}



const { li, label, input } = require('../../helpers/tags')

module.exports = data =>
  li(
    label(
      {
        className: `form-field--select__label${
          data.disabled ? ' form-field--select__label--disabled' : ''
        }`,
      },
      input({
        type: data.multiple ? 'checkbox' : 'radio',
        value: data.value || '',
        name: data.name,
        checked: data.checked,
        disabled: data.disabled || false,
      }),
      ' ',
      data.label
    )
  )




const { textarea } = require('../../helpers/tags')

module.exports = data =>
  textarea(
    {
      id: `ff-${data.name}`,
      name: data.name,
      placeholder: data.placeholder || '',
      cols: data.cols || 40,
      rows: data.rows || 4,
    },
    data.value || ''
  )




*/
