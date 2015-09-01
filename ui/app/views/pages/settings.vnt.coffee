broker = require('../../modules/broker')
actions = require('../../modules/actions')
{getFormValues} = require('../../modules/auxiliaries')

module.exports = broker.add({
    'submit #settings form': (e, el) ->
        e.preventDefault() if e
        actions.updateUser(getFormValues(el))
})
