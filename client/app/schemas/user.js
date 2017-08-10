const {
    required,
    email,
    minlength,
    isOneOf,
} = require('../modules/validations')

module.exports = {
    name: {
        type: 'text',
        validations: [required],
    },
    email: {
        type: 'email',
        validations: [required, email],
    },
    password: {
        type: 'password',
        validations: [required, [minlength, 8]],
    },
    'settings.email_frequency': {
        type: 'select',
        multiple: false,
        options: [
            {
                value: 'immediate',
            },
            {
                value: 'daily',
            },
            {
                value: 'weekly',
            },
            {
                value: 'never',
            },
        ],
        validations: [
            required,
            [isOneOf, 'immediate', 'daily', 'weekly', 'never'],
        ],
    },
}
