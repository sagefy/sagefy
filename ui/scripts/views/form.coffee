define([
    'jquery'
    'backbone'
    'underscore'
    'modules/mixins'
    'hbs/components/forms/form'
    'hbs/components/forms/field'
], ($, Bb, _, mixins, formTemplate, fieldTemplate) ->

    class FormView extends Backbone.View

        el: $('.page')
        events: {
            'submit form': 'submit'
            'keyup input': 'validateField'
        }

        formTemplate: formTemplate
        fieldTemplate: fieldTemplate

        initialize: (options = {}) ->
            if @beforeInitialize
                @beforeInitialize()

            if options.model
                @model = options.model

            if @model and @mode == "edit"
                @model.fetch()

            @listenTo(@model, 'error', @error)
            @listenTo(@model, 'invalid', @invalid)
            @listenTo(@model, 'sync', @sync)

            if @onInitialize
                @onInitialize()

            if @mode != "edit"
                @render()

        _getFields: ->
            if @fields
                return _.filter(@model.fields, (field) =>
                    return field.name in @fields
                )

            return @model.fields

        render: ->
            fields = ""
            for field in @_getFields()
                fields += @fieldTemplate(
                    $.extend(true, {}, field, {
                        inputTypeFields: ['text', 'email', 'password']
                    })
                )

            html = @formTemplate({
                fields: fields
                title: @title
                description: @description
                presubmit: @presubmit
                submitIcon: @submitIcon or 'check'
                submitLabel: @submitLabel or 'Submit'
                mode: @mode
            })

            @$el.html(html)
            @$form = @$el.find('form')

            if @addID
                @$el.attr('id', @addID)

            if @onRender
                @onRender()

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


)
