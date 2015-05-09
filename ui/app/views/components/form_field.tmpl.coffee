module.exports = (data) ->
    classes = [
        'form-field'
        'form-field--' + data.type
        'form-field--' + data.name
    ].join(' ')

    html = "<div class=\"#{classes}\">"

    if data.label and data.type not in ['button', 'submit']
        html += require('./form_field_label.tmpl')(data)

    switch data.type
        when 'text', 'email', 'password'
            html += require('./form_field_input.tmpl')(data)
        when 'textarea'
            html += require('./form_field_textarea.tmpl')(data)
        when 'submit', 'button'
            html += require('./form_field_button.tmpl')(data)
        when 'select'
            html += '<div class="select-wrap"></div>'

    if data.description
        html += "<p class=\"form-field__description\">#{data.description}</p>"

    return html + '</div>'
