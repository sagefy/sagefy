const {div, p, span} = require('../../modules/tags')
const icon = require('./icon.tmpl')

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
        nodes.push(require('./form_field_label.tmpl')(data))
    }

    if(['text', 'email', 'number', 'password', 'hidden']
        .indexOf(data.type) > -1) {
        nodes.push(require('./form_field_input.tmpl')(data))
    }
    if(['textarea'].indexOf(data.type) > -1) {
        nodes.push(require('./form_field_textarea.tmpl')(data))
    }
    if(['submit', 'button'].indexOf(data.type) > -1) {
        nodes.push(require('./form_field_button.tmpl')(data))
    }
    if(['select'].indexOf(data.type) > -1) {
        nodes.push(require('./form_field_select.tmpl')(data))
    }
    if(['list'].indexOf(data.type) > -1) {
        nodes.push(require('./form_field_list.tmpl')(data))
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
