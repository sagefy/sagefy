FormView = require('./form')
UserModel = require('../models/user')
mixins = require('../modules/mixins')

module.exports = class CreatePasswordView extends FormView
    title: 'Create a New Password'
    addID: 'create-password'
    fields: []  # Step 1: Email, otherwise none
    submitLabel: 'Send Email'
    submitIcon: 'envelope'
    mode: ''

    beforeInitialize: ->
        @model = new UserModel()
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

    onRender: ->
        @updatePageWidth(6)

    submit: (e) ->
        e.preventDefault()
        data = @formData(@$form)
        @model.getPasswordToken(data)
        # @model.setPassword(data)

    updatePageWidth: mixins.updatePageWidth
