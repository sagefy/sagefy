const { div, h1, p } = require('../../modules/tags')
const form = require('../components/form.tmpl')
const userSchema = require('../../schemas/user')
const { extend } = require('../../modules/utilities')
const { createFieldsData } = require('../../modules/auxiliaries')
const wizard = require('../components/wizard.tmpl')

const emailFields = [{
    name: 'email',
    label: 'Email',
    description: 'We need your email to send the token.',
    placeholder: 'ex: unicorn@example.com',
}, {
    type: 'submit',
    name: 'submit',
    label: 'Send Token',
    icon: 'create',
}]

emailFields.forEach((field, index) => {
    emailFields[index] = extend({}, userSchema[field.name] || {}, field)
})

const passwordFields = [{
    name: 'password',
    label: 'Password',
}, {
    type: 'submit',
    name: 'submit',
    label: 'Change Password',
    icon: 'create',
}]

passwordFields.forEach((field, index) => {
    passwordFields[index] = extend({}, userSchema[field.name] || {}, field)
})

module.exports = (data) => {
    // TODO-3 the state should be provided solely by data,
    //      the view should not be looking at the window query string
    const { token, id } = data.routeQuery
    const state = token && id ? 'password'
            : data.passwordPageState || 'email'
    return div(
        {
            id: 'password',
            className: `page ${state}`,
        },
        h1('Create a New Password'),
        wizard({
            options: [
                { name: 'email', label: 'Enter Email' },
                { name: 'inbox', label: 'Check Inbox' },
                { name: 'password', label: 'Change Password' },
            ],
            state,
        }),
        getNodesForState(state, data)
    )
}

const getNodesForState = (state, data) => {
    let instanceFields
    if (state === 'email') {
        instanceFields = createFieldsData({
            schema: userSchema,
            fields: emailFields,
            errors: data.errors,
            formData: data.formData,
            sending: data.sending,
        })
        return form(instanceFields)
    }
    if (state === 'inbox') {
        return p('Check your inbox. Be sure to check your spam folder.')
    }
    if (state === 'password') {
        instanceFields = createFieldsData({
            schema: userSchema,
            fields: passwordFields,
            errors: data.errors,
            formData: data.formData,
            sending: data.sending,
        })
        return form(instanceFields)
    }
}
