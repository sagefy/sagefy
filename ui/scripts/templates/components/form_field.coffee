module.exports = (data) ->
    classes = [
        'form-field'
        'form-field--' + data.type
        'form-field--' + data.name
    ].join(' ')

    html = "<div class=\"#{classes}\">"

    if data.title
        html += require('./form_field_label')(data)

    switch data.type
        when 'text', 'email', 'password'
            html += require('./form_field_input')(data)
        when 'submit', 'button'
            html += require('./form_field_button')(data)
        when 'select'
            html += require('./select')(data)

    if data.description
        html += "<p class=\"form-field__description\">#{data.description}</p>"

    return html + '</div>'
