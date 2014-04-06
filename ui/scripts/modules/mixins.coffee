define([
    'underscore'
], (_) ->

    {
        formData: ($form) ->
            _($form.serializeArray()).reduce((obj, field) ->
                obj[field.name] = field.value
                obj
            , {})

        isLoggedIn: ->
            false
    }

)
