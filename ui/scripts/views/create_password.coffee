FormView = require('./form')
mixins = require('../modules/mixins')

class CreatePasswordView extends FormView
    title: 'Create a New Password'
    id: 'create-password'
    className: 'col-6'
    fields: ['email']  # Step 1: Email, otherwise none
    submitLabel: 'Send Email'
    submitIcon: 'envelope'
    mode: ''

    initialize: (options) ->
        @listenTo(@model, 'passwordToken', @tokenSent)
        @listenTo(@model, 'errorPasswordToken', @error)
        @listenTo(@model, 'change:password', @passwordUpdated)
        # TODO: determine mode
        super(options)

    error: (errors) =>
        @invalid(undefined, errors)

    tokenSent: ->
        # TODO: go to step 2

    passwordUpdated: ->
        # TODO: go to step 4

    submit: (e) ->
        if e
            e.preventDefault()
        data = @formData(@$form)

        errors = @model.validate(data, {fields: @fields})

        if errors
            @displayErrors(errors)
        else
            @model.getPasswordToken(data)
            # @model.set('password', data.password)
            # @model.save()


module.exports =  CreatePasswordView
