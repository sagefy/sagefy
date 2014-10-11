FormAdapter = require('./form')
UserModel = require('../models/user')
FormView = require('../views/components/form')
FormLayoutView = require('../views/layouts/form')
_ = require('../framework/utilities')

class SettingsAdapter extends FormAdapter
    url: '/settings'
    title: 'Settings'
    requireLogin: true

    render: ->
        super
        @model = new UserModel()
        @form = new FormView({fields: @getFields()})
        @view = new FormLayoutView({
            id: 'settings'
            className: 'col-6'
            region: @page
        })
        @view.render({
            title: 'Settings'
        })
        @view.form.appendChild(@form.el)

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

    getFields: ->
        fields = [{
            name: 'name'
            title: 'Username'
            placeholder: 'ex: Unicorn'
        }, {
            name: 'email'
            title: 'Email'
            placeholder: 'ex: unicorn@example.com'
        }, {
            title: 'Password'
            type: 'message'
            description: '<a href="/password">Change your password here</a>.'
        }, {
            type: 'submit'
            label: 'Update'
            icon: 'check'
        }]
        for field in fields
            _.extend(field, @model.fields[field.name] or {})
        return fields

    showForm: ->
        @form.render(@model.attributes)

    error: (errors) ->
        if _.isArray(errors)
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
