define([
    'underscore'
], (_) ->

    parseJSON = (str) ->
        try
            return JSON.parse(str)
        catch e
            return str

    {
        formData: ($form) ->
            _($form.serializeArray()).reduce((obj, field) ->
                obj[field.name] = field.value
                obj
            , {})

        isLoggedIn: ->
            false

        parseJSON: parseJSON

        parseAjaxError: (error) ->
            return parseJSON(error.responseText)

        validateModelFromFields: (attrs, options) ->
            for field, validations of @fields  # where @ is model
                value = attrs[field]

                if validations.required and not value
                    return "Please enter #{field}"

                if validations.email and not /\S+@\S+\.\S+/.test(value)
                    return "Please enter a valid email address."

                if validations.minlength and value.length < validations.minlength
                    return "Please enter at least #{validations.minlength} in #{field}."

    }

)
