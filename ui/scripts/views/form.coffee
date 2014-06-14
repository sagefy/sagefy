$ = require('jquery')
Backbone = require('backbone')
_ = require('underscore')
mixins = require('../modules/mixins')
formTemplate = require('../../templates/components/forms/form')
fieldTemplate = require('../../templates/components/forms/field')

class FormView extends Backbone.View
    events: {
        'submit form': 'submit'
        'keyup input': 'validateField'
    }

    formTemplate: formTemplate
    fieldTemplate: fieldTemplate

    initialize: (options = {}) ->
        @$region = options.$region || $({})

        if options.model
            @model = options.model

        if @beforeInitialize
            @beforeInitialize()

        if @model and @mode == "edit"
            @model.fetch()

        @listenTo(@model, 'error', @error)
        @listenTo(@model, 'invalid', @invalid)
        @listenTo(@model, 'sync', @sync)

        if @onInitialize
            @onInitialize()

        if @mode != "edit"
            @render()

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

        if @onRender
            @onRender()

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

    _displayErrors: (errors = []) ->
        for error in errors
            $field = @$form
                .find("[name=\"#{error.name}\"]")
                .closest('.form-field')
            @_showError($field, error)

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

    _showValid: ($field) ->
        $field
            .removeClass('form-field--error')
            .addClass('form-field--success')
            .find('.form-field__feedback')
                .remove()

    validateField: _.debounce((e) ->
        $input = $(e.currentTarget)
        $field = $input.closest('.form-field')
        name = $input.attr('name')
        field = _(@_getFields()).findWhere({ name: name })
        value = $input.val()
        error = @fieldHasError(field, value)
        if error
            @_showError($field, error)
        else
            @_showValid($field)
    , 250)

    error: (model, response) ->
        @$form.find(':submit').removeAttr('disabled')
        errors = @parseAjaxError(response).errors
        @_displayErrors(errors)

        if @onError
            @onError()

    invalid: (model, errors) ->
        @$form.find(':submit').removeAttr('disabled')
        @_displayErrors(errors)

        if @onInvalid
            @onInvalid()

    submit: (e) ->
        e.preventDefault()
        @model.save(@formData(@$form))
        @$form.find(':submit').attr('disabled', 'disabled')

        if @onSubmit
            @onSubmit()

    sync: ->
        if @onSync
            @onSync()

    formData: mixins.formData
    fieldHasError: mixins.validateField
    parseAjaxError: mixins.parseAjaxError


module.exports = FormView
