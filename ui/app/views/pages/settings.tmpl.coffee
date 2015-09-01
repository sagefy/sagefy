{div, h1, a} = require('../../modules/tags')
c = require('../../modules/content').get
userSchema = require('../../schemas/user')
{extend} = require('../../modules/utilities')
form = require('../components/form.tmpl')
{mergeFieldsData} = require('../../modules/auxiliaries')

fields = [{
    name: 'id'
    type: 'hidden'
}, {
    name: 'name'
    label: 'Name'
    placeholder: 'ex: Unicorn'
}, {
    name: 'email'
    label: 'Email'
    placeholder: 'ex: unicorn@example.com'
}, {
    name: 'password'
    label: 'Password'
    type: 'message'
    description: a(
        {href: '/password'}
        'Change your password here.'
    )
}, {
    name: 'avatar'
    label: 'Avatar'
    type: 'message'
    description: a(
        {href: 'http://gravatar.com'}
        'Update your avatar on Gravatar.'
    )
}, {
    name: 'submit'
    type: 'submit'
    label: 'Update'
    icon: 'check'
}]

for index, field of fields
    fields[index] = extend({}, userSchema[field.name], field)

module.exports = (data) ->
    user = data.users?[data.currentUserID]
    return div({className: 'spinner'}) unless user

    fields_ = mergeFieldsData(
        fields
        extend({formData: user}, data)
    )

    return div(
        {id: 'settings', className: 'col-6'}
        h1('Settings')
        form(fields_)
    )
