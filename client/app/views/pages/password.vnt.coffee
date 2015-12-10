broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{getFormValues} = require('../../modules/auxiliaries')
qs = require('../../modules/query_string')

module.exports = broker.add({
    'submit #password.email form': (e, el) ->
        e.preventDefault() if e
        tasks.getUserPasswordToken(getFormValues(el))

    'submit #password.password form': (e, el) ->
        e.preventDefault() if e
        {token, id} = qs.get()
        data = getFormValues(el)
        data.token = token
        data.id = id
        tasks.createUserPassword(data)
})
