FormView = require('./form')
mixins = require('../modules/mixins')

class CreatePasswordView extends FormView
    title: 'Create a New Password'
    id: 'create-password'
    className: 'max-width-6'
    fields: []  # Step 1: Email, otherwise none
    submitLabel: 'Send Email'
    submitIcon: 'envelope'
    mode: ''

    beforeInitialize: ->
        @listenTo(@model, 'passwordToken', @tokenSent)
        @listenTo(@model, 'errorPasswordToken', @error)
        @listenTo(@model, 'change:password', @passwordUpdated)
        # TODO: determine mode

    error: (errors) =>
        @invalid(undefined, errors)

    tokenSent: ->
        # TODO: go to step 2

    passwordUpdated: ->
        # TODO: go to step 4

    submit: (e) ->
        e.preventDefault()
        data = @formData(@$form)
        @model.getPasswordToken(data)
        # @model.set('password', data.password)
        # @model.save()


module.exports =  CreatePasswordView
