{div, h1, p, a, hr} = require('../../modules/tags')
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
    icon: 'check'
}]

for index, field of fields
    fields[index] = extend({}, userSchema[field.name], field)

module.exports = (data) ->
    user = data.users?[data.currentUserID]
    return div({className: 'spinner'}) unless user

    fields_ = mergeFieldsData(
        fields
        extend({
            formData: {
                id: user.id
                name: user.name
                email: user.email
                'settings.email_frequency': user.settings.email_frequency
            }
        }, data)
    )

    return div(
        {id: 'settings', className: 'col-6'}
        h1('Settings')
        form(fields_)
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
