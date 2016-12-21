const {div, h1, p, a, br} = require('../../modules/tags')
const form = require('../components/form.tmpl')
const icon = require('../components/icon.tmpl')
const userSchema = require('../../schemas/user')
const {extend} = require('../../modules/utilities')
const {createFieldsData} = require('../../modules/auxiliaries')

const fields = [{
    name: 'name',
    label: 'Name',
    placeholder: 'ex: Unicorn',
}, {
    name: 'email',
    label: 'Email',
    description: 'We need your email to send notices ' +
                 'and to reset your password.',
    placeholder: 'ex: unicorn@example.com',
}, {
    name: 'password',
    label: 'Password',
}, {
    name: 'submit',
    label: 'Sign Up',
    type: 'submit',
    icon: 'sign-up',
}]

fields.forEach((field, index) => {
    fields[index] = extend({}, userSchema[field.name] || {}, field)
})

module.exports = (data) => {
    if (data.currentUserID) { return div('Logged in already.') }

    const instanceFields = createFieldsData({
        schema: userSchema,
        fields,
        errors: data.errors,
        formData: data.formData,
        sending: data.sending,
    })

    return div(
        {id: 'sign-up', className: 'page'},
        h1('Sign Up'),
        p(
            'Already have an account? ',
            a(
                {href: '/log_in'},
                icon('log-in'),
                ' Log In'
            ),
            '.',
            br(),
            'By signing up, you agree to our ',
            a(
                {href: '/terms'},
                icon('terms'),
                ' Terms of Service'
            ),
            '.'
        ),
        form(instanceFields)
    )
}
