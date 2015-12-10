broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{getFormValues} = require('../../modules/auxiliaries')

module.exports = broker.add({
    'submit #settings form': (e, el) ->
        e.preventDefault() if e
        tasks.updateUser(getFormValues(el))
})
