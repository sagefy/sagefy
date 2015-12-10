broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{getFormValues} = require('../../modules/auxiliaries')

module.exports = broker.add({
    'submit #sign-up form': (e, el) ->
        e.preventDefault() if e
        tasks.createUser(getFormValues(el))

    'keyup #sign-up input': (e, el) ->
        # TODO tasks.validateFormField({})
})
