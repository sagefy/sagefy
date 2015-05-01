module.exports = {
    name: {
        type: 'text'
        validations: {
            required: true
        }
    }
    email: {
        type: 'email'
        validations: {
            required: true
            email: true
        }
    }
    password: {
        type: 'password'
        validations: {
            required: true
            minlength: 8
        }
    }
}
