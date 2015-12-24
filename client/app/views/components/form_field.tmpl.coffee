{div, p, i, span} = require('../../modules/tags')

module.exports = (data) ->
    classes = [
        'form-field'
        'form-field--' + data.type
        'form-field--' + data.name
        'form-field--bad' if data.error
        'form-field--good' if data.good
    ].join(' ')

    return div(
        {className: classes}
        m(data)
    )

m = (data) ->
    nodes = []

    if data.label and data.type not in ['button', 'submit']
        nodes.push(require('./form_field_label.tmpl')(data))

    nodes.push(
        switch data.type
            when 'text', 'email', 'password', 'hidden'
                require('./form_field_input.tmpl')(data)
            when 'textarea'
                require('./form_field_textarea.tmpl')(data)
            when 'submit', 'button'
                require('./form_field_button.tmpl')(data)
            when 'select'
                require('./form_field_select.tmpl')(data)
            when 'list'
                require('./form_field_list.tmpl')(data)
    )

    if data.error
        nodes.push(span(
            {className: 'form-field__feedback'}
            i({className: 'fa fa-ban'})
            data.error
        ))

    if data.description
        nodes.push(
            p({className: 'form-field__description'}, data.description)
        )

    return nodes
