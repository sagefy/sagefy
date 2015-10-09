{div, h1, p, a, i, br} = require('../../modules/tags')
form = require('../components/form.tmpl')
userSchema = require('../../schemas/user')
{extend} = require('../../modules/utilities')
{mergeFieldsData} = require('../../modules/auxiliaries')

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
    icon: 'user'
}]

for index, field of fields
    fields[index] = extend({}, userSchema[field.name], field)

module.exports = (data) ->
    fields_ = mergeFieldsData(fields, data)

    return div(
        {id: 'sign-up', className: 'col-6'}
        h1('Sign Up')
        p(
            'Already have an account? '
            a(
                {href: '/log_in'}
                i({className: 'fa fa-sign-in'})
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
        form(fields_)
    )
