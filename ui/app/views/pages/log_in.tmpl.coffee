{div, h1, p, br, a, i} = require('../../modules/tags')
form = require('../components/form.tmpl')
userSchema = require('../../schemas/user')
{extend} = require('../../modules/utilities')
{mergeFieldsData} = require('../../modules/auxiliaries')

fields = [{
    name: 'name'
    label: 'Name'
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

for index, field of fields
    fields[index] = extend({}, userSchema[field.name], field)

module.exports = (data) ->
    fields_ = mergeFieldsData(fields, data)

    return div(
        {id: 'log-in', className: 'col-6'}
        h1('Log In')
        p(
            'Don\'t have an account? '
            a(
                {href: '/sign_up'}
                i({className: 'fa fa-user'})
                ' Sign Up'
            )
            '.'
            br()
            'Forgot your password? '
            a(
                {href: '/password'}
                i({className: 'fa fa-refresh'})
                ' Reset'
            )
            '.'
        )
        form(fields_)
    )
