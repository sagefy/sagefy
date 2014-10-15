FormAdapter = require('./form')
UserModel = require('../models/user')
View = require('../framework/view')
FormView = require('../views/components/form')
FormLayoutView = require('../views/layouts/form')
_ = require('../framework/utilities')
queryString = require('../modules/query_string')

# TODO: trans

class PasswordAdapter extends FormAdapter
    url: '/password'
    title: 'Create a New Password'

    render: ->
        super
        @model = new UserModel()
        @view = new FormLayoutView({
            id: 'password'
            className: 'col-8'
            region: @page
        })
        @changeState(@getState())

    remove: ->
        @view.remove()
        @form.remove()
        @model.remove()
        super

    getState: ->
        qs = window.location.search
        if qs.indexOf('token') > -1
            @state = 'password'
        else
            @state = 'email'
        return @state

    changeState: (state) ->
        if state in ['password', 'email']
            @form = new FormView({fields: @getFields(state)})
        else
            @form = new View({
                template: -> return "Check your inbox. " +
                                    "If not, check your spam folder."
            })
        @form.render()
        @view.render({
            title: 'Change Password'
            description: @getDescription(state)
        })
        @view.form.appendChild(@form.el)
        @bindEvents()

    bindEvents: ->
        @stopListening()
        @listenTo(@model, 'passwordToken', @toInbox.bind(this))
        @listenTo(@model, 'createPassword', @toDashboard.bind(this))
        @listenTo(@model, 'error', @error.bind(this))
        @listenTo(@form, 'submit', @post.bind(this))

    getFields: (state) ->
        if state is 'email'
            fields = [{
                name: 'email'
                title: 'Email'
                description: 'We need your email to send the token.'
                placeholder: 'ex: unicorn@example.com'
            }, {
                type: 'submit'
                label: 'Send Token'
                icon: 'envelope'
            }]
        else if state is 'password'
            fields = [{
                name: 'password'
                title: 'Password'
            }, {
                type: 'submit'
                label: 'Change Password'
                icon: 'check'
            }]
        for field in fields
            _.extend(field, @model.fields[field.name] or {})
        return fields

    getDescription: (state) ->
        steps = [{
            name: 'email'
            title: '1. Enter Email'
        }, {
            name: 'inbox'
            title: '2. Check Inbox'
        }, {
            name: 'password'
            title: '3. Change Password'
        }]
        html = '<nav class="wizard"><ol>'
        for step in steps
            className = if step.name is state then 'selected' else ''
            html += "<li class=\"#{className}\">"
            html += step.title
            html += '</li>'
        html += '</ol></nav>'
        return html

    toInbox: ->
        @changeState('inbox')

    toDashboard: ->
        # Hard refresh to get the cookie
        window.location = '/dashboard'

    error: (errors) ->
        if _.isArray(errors)
            @form.errorMany(errors)
        else
            window.alert(errors)

    post: ->
        if @state is 'email'
            @model.getPasswordToken(@form.getValues())
        else if @state is 'password'
            qs = queryString()
            @model.createPassword(_.extend({
                id: qs.id
                token: qs.token
            }, @form.getValues()))

module.exports = PasswordAdapter
