broker = require('../../modules/broker')
actions = require('../../modules/actions')
{getFormValues} = require('../../modules/auxiliaries')

module.exports = broker.add({
    'submit #log-in form': (e, el) ->
        e.preventDefault() if e
        actions.logInUser(getFormValues(el))
})
