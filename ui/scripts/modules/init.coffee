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

            $.validator.addMethod(
                'password'
                (value) ->
                    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/.test(value)
                "Enter a valid password."
            )
    }
)
