define([
    'underscore'
], (_) ->

    parseJSON = (str) ->
        try
            return JSON.parse(str)
        catch e
            return str

    validEmail = (val) ->
        return /\S+@\S+\.\S+/.test(val)

    return {
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
            errors = []

            for field in @fields  # where @ is model
                val = attrs[field.name]
                test = field.validations

                if test.required and not val
                    errors.push({
                        name: field.name
                        message: "Please enter #{field}"
                    })

                if test.email and not validEmail(val)
                    errors.push({
                        name: field.name
                        message: "Please enter a valid email address."
                    })

                if test.minlength and val.length < test.minlength
                    errors.push({
                        name: field.name
                        message: "Please enter at least #{validations.minlength} in #{field}."
                    })

            if errors.length
                return errors

    }

)
