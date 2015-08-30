{div, h1, nav, ol, li, a} = require('../../modules/tags')
form = require('../components/form.tmpl')
userSchema = require('../../schemas/user')
{extend} = require('../../modules/utilities')

module.exports = ->
    return div(
        {id: 'password', className: 'col-8'}
        h1('Create a New Password')
        ol(
            {className: 'wizard'}
            li(
                {href: '#', className: 'email selected'}
                'Enter Email'
            )
            li(
                {href: '#', className: 'inbox'}
                'Check Inbox'
            )
            li(
                {href: '#', className: 'password'}
                'Change Password'
            )
        )
        form([])
    )

getSchema = (state) ->
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


'Check your inbox. If not, check your spam folder.'


getState = ->
    qs = window.location.search
    if qs.indexOf('token') > -1
        @state = 'password'
    else
        @state = 'email'
    return @state
