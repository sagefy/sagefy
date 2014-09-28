View = require('../../framework/view')
fieldTemplate = require('../../templates/components/form_field')
_ = require('../../framework/utilities')

# Generic Form View
# Designed to be extended
class FormView extends View
    # Validates all fields on submit
    # Validates single fields on change
    domEvents: {
        'submit form': 'submit'
        'keyup input': 'change'
    }

    tagName: 'form'
    fieldTemplate: fieldTemplate

    # Setup the fields for display
    constructor: (options) ->
        super
        @fields = options.fields

    # As there's no template... instead the HTML is
    # the composition of the fields
    render: (data) ->
        super
        @el.innerHTML = @getFieldsHTML()

    # Iterates over each field specified
    # And generates the fields HTML
    getFieldsHTML: ->
        html = ''
        for field in @fields
            html += @fieldTemplate(field)
        return html

    # Returns an object of the fields in the format:
    # {name: value, name: value}
    # From HTML to Model `set`/`save`
    getValues: ->
        data = {}
        for field in @getFields()
            data[field.name] = @getValue(field)
        return data

    getValue: (field) ->
        switch field.tagName.toLowerCase()
            when 'input'
                return field.value
            when 'textarea'
                return field.value
            when 'select'
                return field.options[field.selectedIndex].value

    getFields: ->
        return @el.querySelectorAll('input, textarea, select')

    getField: (fieldName) ->
        input = @el.querySelector("[name=\"#{fieldName}\"]")
        return _.closest(input, @el, '.form-field')

    # Communicate that the form has been submitted
    submit: (e) ->
        e.preventDefault() if e
        @trigger('submit', @getValues())
        @disable()

    disable: ->
        @form.querySelector('[type="submit"]')
            .setAttribute('disabled', 'disabled')

    enable: ->
        @form.querySelector('[type="submit"]')
            .setAttribute('disabled', '')

    change: _.debounce((e) ->
        @trigger('validate', e.target.name, e.target.value)
    , 200)

    error: (fieldName, error) ->
        return @errorField(@getField(fieldName), error)

    # Adds an error message to a single form field
    errorField: (field, error) ->
        field.classList.remove('form-field--success')
        field.classList.add('form-field--error')
        field.removeChild(field.querySelector('.form-field__feedback'))
        feedback = @createElement({
            tagName: 'span'
            className: 'form-field__feedback'
        })
        feedback.innerHTML = """
            <i class="fa fa-ban"></i>
            #{error.message}
        """
        field.appendChild(feedback)

    # Given an array of errors,
    # Shows those errors on the form
    errorMany: (errors = []) ->
        @enable()
        for error in errors
            field = @getField(error.name)
            @errorField(field, error)

    clear: (fieldName) ->
        return @clearField(@getField(fieldName))

    # Removes error messages to a single form field
    clearField: (field) ->
        field.classList.remove('form-field--error')
        field.classList.add('form-field--success')
        field.removeChild(field.querySelector('.form-field__feedback'))

    clearAll: ->
        for field in @getFields()
            @clearField(field)

module.exports = FormView
