broker = require('../../modules/broker')
actions = require('../../modules/actions')
{getFormValues} = require('../../modules/auxiliaries')
qs = require('../../modules/query_string')

module.exports = broker.add({
    'submit #password.email form': (e, el) ->
        e.preventDefault() if e
        actions.getUserPasswordToken(getFormValues(el))

    'submit #password.password form': (e, el) ->
        e.preventDefault() if e
        {token, id} = qs.get()
        data = getFormValues(el)
        data.token = token
        data.id = id
        actions.createUserPassword(data)
})
