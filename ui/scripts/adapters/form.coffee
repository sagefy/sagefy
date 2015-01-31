PageAdapter = require('./page')
util = require('../framework/utilities')

class FormAdapter extends PageAdapter
    remove: ->
        @view.remove() if @view
        @form.remove() if @form
        @model.remove() if @model
        super

    bindEvents: ->
        @stopListening()
        return if not @model or not @form
        @listenTo(@model, 'invalid', @error.bind(this))
        @listenTo(@model, 'error', @error.bind(this))
        @listenTo(@form, 'submit', @validate.bind(this))
        @listenTo(@form, 'change', @validateField.bind(this))

    addModelFields: (fields) ->
        for field in fields
            util.extend(field, @model.fields[field.name] or {})
        return fields

    error: (errors) ->
        if util.isArray(errors)
            @form.errorMany(errors)
        else
            window.alert(errors)  # TODO don't use alert

    validate: ->
        return if not @model
        @model.set(@form.getValues())
        @model.save()

    validateField: (name, value) ->
        return if not @model
        @model.set(name, value)
        error = @model.validateField(name)
        if error
            @form.error(name, {message: error})
        else
            @form.clear(name)

module.exports = FormAdapter
