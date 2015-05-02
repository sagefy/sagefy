FormAdapter = require('./form')
UserModel = require('../models/user')
FormView = require('../views/components/form')
FormLayoutView = require('../views/layouts/form')
util = require('../../framework/utilities')
queryString = require('../modules/query_string')

# TODO trans

class PasswordAdapter extends FormAdapter
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

    getState: ->
        qs = window.location.search
        if qs.indexOf('token') > -1
            @state = 'password'
        else
            @state = 'email'
        return @state

    changeState: (state) ->
        if state in ['password', 'email']
            @form = new FormView({schema: @getSchema(state)})
        else
            @form = new View({
                template: ->
                    return 'Check your inbox. ' +
                           'If not, check your spam folder.'
            })
        @form.render()
        @view.render({
            title: 'Change Password'
            description: @getDescription(state)
        })
        @view.form.appendChild(@form.el)
        @bindEvents()

    bindEvents: ->
        # Fully overwriting method
        @stopListening()
        @listenTo(@model, 'passwordToken', @toInbox.bind(this))
        @listenTo(@model, 'createPassword', @toMySets.bind(this))
        @listenTo(@model, 'error', @error.bind(this))
        @listenTo(@form, 'submit', @post.bind(this))

    getSchema: (state) ->
        if state is 'email'
            schema = [{
                name: 'email'
                label: 'Email'
                description: 'We need your email to send the token.'
                placeholder: 'ex: unicorn@example.com'
            }, {
                type: 'submit'
                name: 'submit'
                label: 'Send Token'
                icon: 'envelope'
            }]
        else if state is 'password'
            schema = [{
                name: 'password'
                label: 'Password'
            }, {
                type: 'submit'
                name: 'submit'
                label: 'Change Password'
                icon: 'check'
            }]
        return @addModelSchema(schema)

    getDescription: (state) ->
        # TODO should this be a template?
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

    toMySets: ->
        # Hard refresh to get the cookie
        window.location = '/my_sets'

    post: ->
        if @state is 'email'
            @model.getPasswordToken(@form.getValues())
        else if @state is 'password'
            qs = queryString.get()
            @model.createPassword(util.extend({
                id: qs.id
                token: qs.token
            }, @form.getValues()))

module.exports = PasswordAdapter
