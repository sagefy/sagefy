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
        }

        formTemplate: formTemplate
        fieldTemplate: fieldTemplate

        initialize: (options = {}) ->
            if @beforeInitialize
                @beforeInitialize()

            if options.model
                @model = options.model

            if @model and options.mode == "edit"
                @model.fetch()

            @listenTo(@model, 'error', @error)
            @listenTo(@model, 'invalid', @invalid)

            if @onInitialize
                @onInitialize()

            if options.mode != "edit"
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
            })

            @$el.html(html)
            @$el.addClass('max-width-8')
            @$form = @$el.find('form')

            if @addID
                @$el.attr('id', @addID)

            if @onRender
                @onRender()

        _displayErrors: (errors) ->
            console.log('_displayErrors', errors)

            for error in errors
                $field = @$form
                    .find("[name=\"#{error.name}\"]")
                    .closest('.form-field')
                console.log($field.length)

                $field.addClass('form-field--error')
                $field.append("""
                    <span class="form-field__feedback">
                        <i class="fa fa-ban-circle"></i>
                        #{error.message}
                    </span>
                """)

        error: ->
            if @onError
                @onError()

        invalid: (model, errors) ->
            @_displayErrors(errors)

            if @onInvalid
                @onInvalid()

        submit: (e) ->
            e.preventDefault()

            @model.save(@formData(@$form))

            if @onSubmit
                @onSubmit()

        formData: mixins.formData


)
