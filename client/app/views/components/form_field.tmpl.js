const {div, p, span} = require('../../modules/tags')
const icon = require('./icon.tmpl')

const kindTmpl = {}
kindTmpl.label = require('./form_field_label.tmpl')
kindTmpl.input = require('./form_field_input.tmpl')
kindTmpl.textarea = require('./form_field_textarea.tmpl')
kindTmpl.button = require('./form_field_button.tmpl')
kindTmpl.select = require('./form_field_select.tmpl')
kindTmpl.list = require('./form_field_list.tmpl')
kindTmpl.entities = require('./form_field_entities.tmpl')

module.exports = (data) => {
    const classes = [
        'form-field',
        'form-field--' + data.type,
        'form-field--' + data.name,
        data.error ? 'form-field--bad' : '',
        data.good ? 'form-field--good' : ''
    ].join(' ')
    return div(
        {className: classes},
        m(data)
    )
}

const m = (data) => {
    const nodes = []
    if (data.label && ['button', 'submit'].indexOf(data.type) === -1) {
        nodes.push(kindTmpl.label(data))
    }
    if(['text', 'email', 'number', 'password', 'hidden']
        .indexOf(data.type) > -1) {
        nodes.push(kindTmpl.input(data))
    }
    if(data.type === 'textarea') {
        nodes.push(kindTmpl.textarea(data))
    }
    if(['submit', 'button'].indexOf(data.type) > -1) {
        nodes.push(kindTmpl.button(data))
    }
    if(data.type === 'select') {
        nodes.push(kindTmpl.select(data))
    }
    if(data.type === 'list') {
        nodes.push(kindTmpl.list(data))
    }
    if(data.type === 'entities') {
        nodes.push(kindTmpl.entities(data))
    }
    if (data.error) {
        nodes.push(span(
            {className: 'form-field__feedback'},
            icon('bad'),
            data.error
        ))
    }
    if (data.description) {
        nodes.push(
            p({className: 'form-field__description'}, data.description)
        )
    }
    return nodes
}
