broker = require('../../modules/broker')
actions = require('../../modules/actions')

module.exports = broker.add({

})




FormPageView = require('./_form')
queryString = require('../../modules/query_string')
FormView = require('../components/form')
util = require('../../modules/utilities')

class PasswordPageView extends FormPageView
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
