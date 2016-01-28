{div, h1, p, br, a, i} = require('../../modules/tags')
form = require('../components/form.tmpl')
icon = require('../components/icon.tmpl')
userSchema = require('../../schemas/user')
{extend} = require('../../modules/utilities')
{createFieldsData} = require('../../modules/auxiliaries')

fields = [{
    name: 'name'
    label: 'Name or Email'
    placeholder: 'e.g. Unicorn'
}, {
    name: 'password'
    label: 'Password'
    placeholder: ''
}, {
    type: 'submit'
    name: 'log-in'
    label: 'Log In'
    icon: 'log-in'
}]

for index, field of fields
    fields[index] = extend({}, userSchema[field.name], field)

module.exports = (data) ->
    return div('Logged in already.') if data.currentUserID

    instanceFields = createFieldsData({
        schema: userSchema
        fields: fields
        errors: data.errors
        formData: data.formData
        sending: data.sending
    })

    return div(
        {id: 'log-in'}
        h1('Log In')
        p(
            'Don\'t have an account? '
            a(
                {href: '/sign_up'}
                icon('sign-up')
                ' Sign Up'
            )
            '.'
            br()
            'Forgot your password? '
            a(
                {href: '/password'}
                icon('password')
                ' Reset'
            )
            '.'
        )
        form(instanceFields)
    )
