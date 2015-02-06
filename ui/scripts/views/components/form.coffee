View = require('../../framework/view')
SelectView = require('./select')
fieldTemplate = require('../../templates/components/form_field')
util = require('../../framework/utilities')

# Generic Form View
# Designed to be extended
class FormView extends View
    # Validates schema on submit
    # Validates single field on change
    domEvents: {
        'submit form': 'submit'
        'keyup input': 'change'
    }

    tagName: 'form'
    fieldTemplate: fieldTemplate

    # Setup the schema for display
    constructor: (options = {}) ->
        super
        @schema = options.schema

    # As there's no template... instead the HTML is
    # the composition of the schema
    render: (data = {}) ->
        super
        @el.innerHTML = @getFieldsHTML(data)
        @createSelects()

    # Iterates over each field specified
    # And generates the field HTML
    getFieldsHTML: (data) ->
        html = ''
        for field in util.copy(@schema)
            field.value = data[field.name]
            html += @fieldTemplate(field)
        return html

    # If there are select(s), create the instances
    createSelects: ->
        for field in util.copy(@schema)
            if field.type is 'select'
                select = new SelectView({
                    region: @el.querySelector(
                        '.form-field--' + field.name + ' .select-wrap')
                    name: field.name
                    count: field.options.length
                    url: field.url
                    multiple: field.multiple
                    showInline: field.showInline
                })
                select.render({options: field.options})

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
        return util.closest(input, @el, '.form-field')

    # Communicate that the form has been submitted
    submit: (e) ->
        e.preventDefault() if e
        @disable()
        @trigger('submit', @getValues())

    disable: ->
        @el.querySelector('[type="submit"]')
            .setAttribute('disabled', 'disabled')

    enable: ->
        @el.querySelector('[type="submit"]')
            .removeAttribute('disabled')

    change: util.debounce((e) ->
        @trigger('change', e.target.name, e.target.value)
    , 200)

    error: (fieldName, error) ->
        return @errorField(@getField(fieldName), error)

    # Adds an error message to a single form field
    errorField: (field, error) ->
        field.classList.remove('form-field--success')
        field.classList.add('form-field--error')
        feedback = field.querySelector('.form-field__feedback')
        field.removeChild(feedback) if feedback
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
        feedback = field.querySelector('.form-field__feedback')
        field.removeChild(feedback) if feedback

    clearAll: ->
        for field in @getFields()
            @clearField(field)

module.exports = FormView
