const { div, h1, p, br, a } = require('../../modules/tags')
const form = require('../components/form.tmpl')
const icon = require('../components/icon.tmpl')
const userSchema = require('../../schemas/user')
const { extend } = require('../../modules/utilities')
const { createFieldsData, findGlobalErrors } = require('../../modules/auxiliaries')

const fields = [{
    name: 'name',
    label: 'Name or Email',
    placeholder: 'e.g. Unicorn',
}, {
    name: 'password',
    label: 'Password',
    placeholder: '',
}, {
    type: 'submit',
    name: 'log-in',
    label: 'Log In',
    icon: 'log-in',
}]

fields.forEach((field, index) => {
    fields[index] = extend({}, userSchema[field.name] || {}, field)
})

module.exports = (data) => {
    if (data.currentUserID) { div('Logged in already.') }

    const instanceFields = createFieldsData({
        schema: userSchema,
        fields: fields,
        errors: data.errors,
        formData: data.formData,
        sending: data.sending,
    })

    const globalErrors = findGlobalErrors({
        fields: fields,
        errors: data.errors,
    })

    return div(
        { id: 'log-in', className: 'page' },
        h1('Log In'),
        p(
            'Don\'t have an account? ',
            a(
                { href: '/sign_up' },
                icon('sign-up'),
                ' Sign Up'
            ),
            '.',
            br(),
            'Forgot your password? ',
            a(
                { href: '/password' },
                icon('password'),
                ' Reset'
            ),
            '.'
        ),
        form({
            fields: instanceFields,
            errors: globalErrors,
        })
    )
}
