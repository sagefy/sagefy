{div, h1, nav, ol, li, a, p} = require('../../modules/tags')
form = require('../components/form.tmpl')
userSchema = require('../../schemas/user')
{extend} = require('../../modules/utilities')
{createFieldsData} = require('../../modules/auxiliaries')
qs = require('../../modules/query_string')

emailFields = [{
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

for index, field of emailFields
    emailFields[index] = extend({}, userSchema[field.name], field)

passwordFields = [{
    name: 'password'
    label: 'Password'
}, {
    type: 'submit'
    name: 'submit'
    label: 'Change Password'
    icon: 'check'
}]

for index, field of passwordFields
    passwordFields[index] = extend({}, userSchema[field.name], field)

module.exports = (data) ->
    # TODO the state should be provided solely by data,
    #      the view should not be looking at the window query string
    {token, id} = qs.get()
    state = if token and id then 'password' \
            else data.passwordPageState or 'email'
    return div(
        {
            id: 'password'
            className: 'col-8 ' + state
        }
        h1('Create a New Password')
        ol(
            {className: 'wizard'}
            li(
                {href: '#', className: 'email' +
                    if state is 'email'
                    then ' selected' else ''}
                'Enter Email'
            )
            li(
                {href: '#', className: 'inbox' +
                    if state is 'inbox'
                    then ' selected' else ''}
                'Check Inbox'
            )
            li(
                {href: '#', className: 'password' +
                    if state is 'password'
                    then ' selected' else ''}
                'Change Password'
            )
        )
        getNodesForState(state, data)
    )

getNodesForState = (state, data) ->
    if state is 'email'
        instanceFields = createFieldsData({
            schema: userSchema
            fields: emailFields
            errors: data.errors
            formData: data.formData
            sending: data.sending
        })
        return form(instanceFields)
    if state is 'inbox'
        return p('Check your inbox. Be sure to check your spam folder.')
    if state is 'password'
        instanceFields = createFieldsData({
            schema: userSchema
            fields: passwordFields
            errors: data.errors
            formData: data.formData
            sending: data.sending
        })
        return form(instanceFields)
