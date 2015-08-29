{form} = require('../../modules/tags')

module.exports = (data) ->
    {fields} = data
    return form()



class FormView
    # Iterates over each field specified
    # And generates the field HTML
    getFieldsHTML: (data) ->
        html = ''
        for field in util.copy(@schema)
            field.value = data[field.name]
            html += @fieldTemplate(field)
        return html

    # Adds an error message to a single form field
    errorField: (field, error) ->
        @updateFieldStatus(field, false)

        feedback = @createElement({
            tagName: 'span'
            className: 'form-field__feedback'
        })
        feedback.innerHTML = """
            <i class="fa fa-ban"></i>
            #{error.message}
        """
        field.appendChild(feedback)

    updateFieldStatus: (field, valid = true) ->
        if valid
            field.classList.remove('form-field--bad')
            field.classList.add('form-field--good')
        else
            field.classList.add('form-field--bad')
            field.classList.remove('form-field--good')
        feedback = field.querySelector('.form-field__feedback')
        field.removeChild(feedback) if feedback

    disable: ->
        # TODO make this part of state
        el.querySelector('[type="submit"]')
            .setAttribute('disabled', 'disabled')
        # TODO later .removeAttribute('disabled')
