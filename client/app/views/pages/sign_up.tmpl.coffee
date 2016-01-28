{div, h1, p, a, i, br} = require('../../modules/tags')
form = require('../components/form.tmpl')
icon = require('../components/icon.tmpl')
userSchema = require('../../schemas/user')
{extend} = require('../../modules/utilities')
{createFieldsData} = require('../../modules/auxiliaries')

fields = [{
    name: 'name'
    label: 'Name'
    placeholder: 'ex: Unicorn'
}, {
    name: 'email'
    label: 'Email'
    description: 'We need your email to send notices ' +
                 'and to reset your password.'
    placeholder: 'ex: unicorn@example.com'
}, {
    name: 'password'
    label: 'Password'
}, {
    name: 'submit'
    label: 'Sign Up'
    type: 'submit'
    icon: 'sign-up'
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
        {id: 'sign-up'}
        h1('Sign Up')
        p(
            'Already have an account? '
            a(
                {href: '/log_in'}
                icon('log-in')
                ' Log In'
            )
            '.'
            br()
            'By signing up, you agree to our '
            a(
                {href: '/terms'}
                ' Terms of Service'
            )
            '.'
        )
        form(instanceFields)
    )
