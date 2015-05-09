View = require('../../modules/view')

class FormPageView extends View
    template: require('./form_layout.tmpl')

    constructor: ->
        super
        # @listenTo(@model, 'invalid', @error.bind(this))
        # @listenTo(@model, 'error', @error.bind(this))
        # @listenTo(@form, 'submit', @validate.bind(this))
        # @listenTo(@form, 'change', @validateField.bind(this))

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

module.exports = FormPageView
