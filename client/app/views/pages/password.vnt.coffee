broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{getFormValues, parseFormValues} = require('../../modules/auxiliaries')
qs = require('../../modules/query_string')
userSchema = require('../../schemas/user')

module.exports = broker.add({
    'submit #password.email form': (e, el) ->
        e.preventDefault() if e

        values = getFormValues(el)
        tasks.updateFormData(values)
        errors = tasks.validateForm(values, userSchema, ['email'])
        unless errors?.length
            values = parseFormValues(values)
            tasks.getUserPasswordToken(values)

    'submit #password.password form': (e, el) ->
        e.preventDefault() if e

        {token, id} = qs.get()
        values = getFormValues(el)
        values.token = token
        values.id = id

        tasks.updateFormData(values)
        errors = tasks.validateForm(values, userSchema, ['password'])
        unless errors?.length
            values = parseFormValues(values)
            tasks.createUserPassword(values)
})
