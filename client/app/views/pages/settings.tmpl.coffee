{div, h1, p, a, hr} = require('../../modules/tags')
c = require('../../modules/content').get
userSchema = require('../../schemas/user')
{extend} = require('../../modules/utilities')
{createFieldsData} = require('../../modules/auxiliaries')
form = require('../components/form.tmpl')
spinner = require('../components/spinner.tmpl')

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
    name: 'settings.email_frequency'
    label: 'Email Frequency'
    options: [{
        label: 'Immediate'
    }, {
        label: 'Daily'
    }, {
        label: 'Weekly'
    }, {
        label: 'Never'
    }]
    inline: true
}, {
    name: 'submit'
    type: 'submit'
    label: 'Update'
    icon: 'update'
}]

for index, field of fields
    fields[index] = extend({}, userSchema[field.name], field)

module.exports = (data) ->
    user = data.users?[data.currentUserID]
    return spinner() unless user

    instanceFields = createFieldsData({
        schema: userSchema
        fields: fields
        errors: data.errors
        formData: extend({}, {
            id: user.id
            name: user.name
            email: user.email
            'settings.email_frequency': user.settings.email_frequency
        }, data.formData)
        sending: data.sending
    })

    return div(
        {id: 'settings'}
        h1('Settings')
        form(instanceFields)
        hr()
        p(a(
            {href: '/password'}
            'Change my password.'
        ))
        p(a(
            {href: 'http://gravatar.com'}
            'Update my avatar on Gravatar.'
        ))
    )
