validations = require('../modules/validations')

module.exports = {
    name: {
        type: 'text'
        validations: [
            validations.required
        ]
    }
    email: {
        type: 'email'
        validations: [
            validations.required
            validations.email
        ]
    }
    password: {
        type: 'password'
        validations: [
            validations.required
            [validations.minlength, 8]
        ]
    }
}
