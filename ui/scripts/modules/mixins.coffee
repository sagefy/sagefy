define([
    'underscore'
], (_) ->

    formData = ($form) ->
        _($form.serializeArray()).reduce((obj, field) ->
            obj[field.name] = field.value
            obj
        , {})

    parseJSON = (str) ->
        try
            return JSON.parse(str)
        catch e
            return str

    isLoggedIn = ->
        return !! $.cookie('logged_in')

    parseAjaxError = (error) ->
        return parseJSON(error.responseText).errors or error

    validEmail = (val) ->
        return /\S+@\S+\.\S+/.test(val)

    validateField = (field, val) ->
        test = field.validations

        if test.required and not val
            return {
                name: field.name
                message: "Please enter #{field.name}."
            }

        if test.email and not validEmail(val)
            return {
                name: field.name
                message: "Please enter a valid email address."
            }

        if test.minlength and val.length < test.minlength
            return {
                name: field.name
                message: "Please enter at least #{test.minlength} " +
                    "characters in #{field.name}."
            }

        return false  # `false` meaning there's no error

    validateModelFromFields = (attrs, options) ->
        errors = []

        for field in @fields  # where @ is model
            val = attrs[field.name]

            error = validateField(field, val)
            if error
                errors.push(error)

        if errors.length
            return errors

    ucfirst = (str) ->
        return str.charAt(0).toUpperCase() + str.slice(1)

    underscored = (str) ->
        return str.replace(/[-\s]+/g, '_').toLowerCase()

    updatePageWidth = (width) ->
        $page = $('.page')
        classes = $page.attr('class').match(/max-width-\d/) or []
        for cls in classes
            $page.removeClass(cls)
        if width
            $page.addClass('max-width-' + width)

    return {
        formData: formData
        isLoggedIn: isLoggedIn
        parseJSON: parseJSON
        parseAjaxError: parseAjaxError
        validateField: validateField
        validateModelFromFields: validateModelFromFields
        ucfirst: ucfirst
        underscored: underscored
        updatePageWidth: updatePageWidth
    }

)
