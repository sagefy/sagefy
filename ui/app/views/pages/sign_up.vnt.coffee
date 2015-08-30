broker = require('../../modules/broker')
actions = require('../../modules/actions')
{getFormValues} = require('../../modules/auxiliaries')

module.exports = broker.add({
    'submit #sign-up form': (e, el) ->
        e.preventDefault() if e
        actions.createUser(getFormValues(el))

    'keyup #sign-up input': (e, el) ->
        # TODO actions.validateFormField({})
})
