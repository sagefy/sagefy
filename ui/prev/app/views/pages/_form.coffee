View = require('../../modules/view')
FormView = require('../components/form')
util = require('../../modules/utilities')

class FormPageView extends View
    template: require('./form_layout.tmpl')

    elements: {
        form: '.form'
    }

    constructor: ->
        super

    render: ->
        super
        @form = new FormView({
            schema: @getSchema(@modelSchema)
            region: @form
        })
        @form.render()

    error: (errors) ->
        @form.errorMany(errors) if util.isArray(errors)

    validate: ->
        # @form.getValues()

    validateField: (name, value) ->
        # return if not @model
        # @model.set(name, value)
        # error = @model.validateField(name)
        # if error
        #     @form.error(name, {message: error})
        # else
        #     @form.clear(name)

    remove: ->
        @form.remove if @form
        super

    getSchema: (_) ->
        for i, field of @schema
            @schema[i] = util.extend({}, _[field.name], field)
        return @schema

module.exports = FormPageView
