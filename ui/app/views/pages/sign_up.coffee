FormPageView = require('./_form')
aux = require('../../modules/auxiliaries')
userSchema = require('../../schemas/user')

class SignUpPageView extends FormPageView
    id: 'sign-up'
    className: 'col-6'

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
        # TODO@ return @emit('route', '/my_sets') if @requireLogOut()
        aux.setTitle('Sign Up')
        @render({
            title: 'Sign Up for Sagefy'
            description: '''
                Already have an account?
                <a href="/log_in"><i class="fa fa-sign-in"></i> Log In</a>.
                <br />
                By signing up,
                you agree to our <a href="/terms">Terms of Service</a>.
            '''
        })
        @on('submit form', => @emit('request create user'))
        @on('create user', @toMySets.bind(this))
        @on('error on create user', @form.errorMany.bind(@form))

    toMySets: ->
        # Hard redirect to get the cookie
        window.location = '/my_sets'

module.exports = SignUpPageView
