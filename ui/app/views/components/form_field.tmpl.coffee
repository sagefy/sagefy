module.exports = (data) ->
    classes = [
        'form-field'
        'form-field--' + data.type
        'form-field--' + data.name
    ].join(' ')

    return div(
        {className: classes}
        m(data)
    )

m = (data) ->
    if data.label and data.type not in ['button', 'submit']
        return require('./form_field_label.tmpl')(data)

    switch data.type
        when 'text', 'email', 'password'
            return require('./form_field_input.tmpl')(data)
        when 'textarea'
            return require('./form_field_textarea.tmpl')(data)
        when 'submit', 'button'
            return require('./form_field_button.tmpl')(data)
        when 'select'
            return div({className: 'select-wrap'})

    if data.description
        return p({className: 'form-field__description'}, data.description)
