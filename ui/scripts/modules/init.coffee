define([
    'jquery'
    'validation'
], ($) ->
    {
        configFormValidation: ->
            $.validator.setDefaults({
                errorClass: 'form-field__feedback'

                highlight: (el) ->
                    $(el).closest('.form-field')
                        .addClass('form-field--error')
                        .removeClass('form-field--success')

                unhighlight: (el) ->
                    $(el).closest('.form-field')
                        .addClass('form-field--success')
                        .removeClass('form-field--error')
            })
    }
)
