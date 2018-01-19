const { div, p, span } = require('../../modules/tags')
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
