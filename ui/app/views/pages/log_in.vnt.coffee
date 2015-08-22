broker = require('../../modules/broker')
actions = require('../../modules/actions')

module.exports = broker.add({

})





FormPageView = require('./_form')
FormView = require('../components/form')
aux = require('../../modules/auxiliaries')
userSchema = require('../../schemas/user.coffee')

class LogInPageView extends FormPageView
    schema: [{
        name: 'name'
        label: 'Username'
        placeholder: 'e.g. Unicorn'
    }, {
        name: 'password'
        label: 'Password'
        placeholder: ''
    }, {
        type: 'submit'
        name: 'log-in'
        label: 'Log In'
        icon: 'sign-in'
    }]

    modelSchema: userSchema

    constructor: ->
        @on('submit form', => @emit('request log in user'))
        @on('log in user', @toMySets.bind(this))
        @on('error on log in user', @form.errorMany.bind(@form))

    toMySets: ->
        # Hard redirect to get the cookie
        window.location = '/my_sets'
