broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{getFormValues} = require('../../modules/auxiliaries')

module.exports = broker.add({
    'submit #log-in form': (e, el) ->
        e.preventDefault() if e
        tasks.logInUser(getFormValues(el))
})
