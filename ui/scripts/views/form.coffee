$ = require('jquery')
Backbone = require('backbone')
_ = require('underscore')
mixins = require('../modules/mixins')
formTemplate = require('../../templates/components/forms/form')
fieldTemplate = require('../../templates/components/forms/field')

# Generic Form View
# Designed to be extended
class FormView extends Backbone.View
    # Validates all fields on submit
    # Validates single fields on change
    events: {
        'submit form': 'submit'
        'keyup input': 'validateField'
    }

    formTemplate: formTemplate
    fieldTemplate: fieldTemplate

    # Expects options `model` and `$region`
    initialize: (options = {}) ->
        @$region = options.$region || $({})

        if options.model
            @model = options.model

        # Edit mode on the model will fetch the data to fill in the form
        if @model and @mode == "edit"
            @model.fetch()

        @listenTo(@model, 'error', @error)
        @listenTo(@model, 'invalid', @invalid)
        @listenTo(@model, 'sync', @sync)

        if @mode != "edit"
            @render()

    # Optional fields of `title`, `description`, `presubmit`... render
    # in the markup
    render: ->
        @$el.html(@formTemplate({
            fields: @_getFieldsHTML()
            title: @title
            description: @description
            presubmit: @presubmit
            submitIcon: @submitIcon or 'check'
            submitLabel: @submitLabel or 'Submit'
            mode: @mode
        }))
        @$region.html(@$el)
        @$form = @$el.find('form')

    # Iterates over each field specified
    # And generates the fields HTML
    _getFieldsHTML: ->
        html = ""
        for fieldName in @fields
            html += @fieldTemplate(
                $.extend(true, {}, @model.fields[fieldName], {
                    name: fieldName
                    inputTypeFields: ['text', 'email', 'password']
                })
            )
        return html

    # Given an array of errors,
    # Shows those errors on the form
    displayErrors: (errors = []) ->
        @$form.find('[type="submit"]').removeAttr('disabled')
        for error in errors
            $field = @$form
                .find("[name=\"#{error.name}\"]")
                .closest('.form-field')
            @_showError($field, error)

    # Adds an error message to a single form field
    _showError: ($field, error) ->
        $field
            .removeClass('form-field--success')
            .addClass('form-field--error')
            .find('.form-field__feedback')
                .remove()
        $field.append("""
            <span class="form-field__feedback">
                <i class="fa fa-ban"></i>
                #{error.message}
            </span>
        """)

    # Removes error messages to a single form field
    _showValid: ($field) ->
        $field
            .removeClass('form-field--error')
            .addClass('form-field--success')
            .find('.form-field__feedback')
                .remove()

    # Validates a single form field. Throttled.
    validateField: _.throttle((e) ->
        $input = $(e.currentTarget)
        $field = $input.closest('.form-field')
        name = $input.attr('name')
        field = @model.fields[name]
        value = $input.val()
        error = mixins.validateField(name, field, value)
        if error
            @_showError($field, error)
        else
            @_showValid($field)
    , 100)

    # Ajax error => displayErrors
    error: (model, response) ->
        errors = @parseAjaxErrors(response)
        @displayErrors(errors)

    # Backbone model validate => displayErrors
    invalid: (model, errors) ->
        @displayErrors(errors)

    # Saves the model if possible
    # Communicates to the model the list of fields to validate
    submit: (e) ->
        if e
            e.preventDefault()

        @model.save(@formData(@$form), {fields: @fields})
        @$form.find(':submit').attr('disabled', 'disabled')

    sync: ->

    formData: mixins.formData
    parseAjaxErrors: mixins.parseAjaxErrors

module.exports = FormView
