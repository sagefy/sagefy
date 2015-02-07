FormAdapter = require('./form')
UserModel = require('../models/user')
FormView = require('../views/components/form')
FormLayoutView = require('../views/layouts/form')
util = require('../framework/utilities')

# TODO: move copy to content directory

class SettingsAdapter extends FormAdapter
    url: '/settings'
    title: 'Settings'

    render: ->
        return if @requireLogin()
        super
        @model = new UserModel()
        @view = new FormLayoutView({
            id: 'settings'
            className: 'col-6'
            region: @page
        })
        @view.render({
            title: 'Settings'
        })
        @form = new FormView({
            schema: @getSchema()
            region: @view.form
        })

        @listenTo(@model, 'invalid', @error.bind(this))
        @listenTo(@model, 'error', @error.bind(this))
        @listenTo(@model, 'sync', @showForm.bind(this))
        @listenTo(@form, 'submit', @validate.bind(this))
        @listenTo(@form, 'change', @validateField.bind(this))

        @model.fetch({id: 'current'})

    remove: ->
        @view.remove()
        @form.remove()
        @model.remove()
        super

    getSchema: ->
        return @addModelSchema([{
            name: 'name'
            label: 'Username'
            placeholder: 'ex: Unicorn'
        }, {
            name: 'email'
            label: 'Email'
            placeholder: 'ex: unicorn@example.com'
        }, {
            name: 'password'
            label: 'Password'
            type: 'message'
            description: '<a href="/password">Change your password here</a>.'
        }, {
            name: 'avatar'
            label: 'Avatar'
            type: 'message'
            description: '<a href="http://gravatar.com">' +
                         'Update your avatar here</a>'
        }, {
            name: 'submit'
            type: 'submit'
            label: 'Update'
            icon: 'check'
        }])

    showForm: ->
        @form.render(@model.attributes)

    error: (errors) ->
        if util.isArray(errors)
            @form.errorMany(errors)
        else
            window.alert(errors)

    validate: ->
        @model.set(@form.getValues())
        @model.save({fields: ['name', 'email']})

    validateField: (name, value) ->
        @model.set(name, value)
        error = @model.validateField(name)
        if error
            @form.error(name, {message: error})
        else
            @form.clear(name)

module.exports = SettingsAdapter
