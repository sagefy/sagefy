broker = require('../../modules/broker')
actions = require('../../modules/actions')

module.exports = broker.add({

})





FormPageView = require('./_form')
aux = require('../../modules/auxiliaries')
userSchema = require('../../schemas/user')

class SignUpPageView extends FormPageView

    schema: [{
        name: 'name'
        label: 'Username'
        placeholder: 'ex: Unicorn'
    }, {
        name: 'email'
        label: 'Email'
        description: 'We need your email to send notices ' +
                     '<br />and reset password.'
        placeholder: 'ex: unicorn@example.com'
    }, {
        name: 'password'
        label: 'Password'
    }, {
        name: 'submit'
        label: 'Sign Up'
        type: 'submit'
        icon: 'user'
    }]

    modelSchema: userSchema

    constructor: ->
        super
        @on('submit form', => @emit('request create user'))
        @on('create user', @toMySets.bind(this))
        @on('error on create user', @form.errorMany.bind(@form))

    toMySets: ->
        # Hard redirect to get the cookie
        window.location = '/my_sets'
