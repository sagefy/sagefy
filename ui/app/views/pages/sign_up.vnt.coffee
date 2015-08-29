broker = require('../../modules/broker')
actions = require('../../modules/actions')

# Returns an object of the fields' value
getFormValues = (form) ->
    data = {}
    for field in form.querySelectorAll('input, textarea')
        data[field.name] = field.value
    return data

module.exports = broker.add({
    'submit #sign-up form': (e, el) ->
        e.preventDefault() if e
        actions.createUser(getFormValues(el))

    'keyup #sign-up input': (e, el) ->
        # TODO actions.validateFormField({})
})
