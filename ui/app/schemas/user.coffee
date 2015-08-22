{required, email, minlength} = require('../modules/validations')

module.exports = {
    name: {
        type: 'text'
        validations: [
            required
        ]
    }
    email: {
        type: 'email'
        validations: [
            required
            email
        ]
    }
    password: {
        type: 'password'
        validations: [
            required
            [minlength, 8]
        ]
    }
}
