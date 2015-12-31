broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{getFormValues, parseFormValues} =
    require('../../modules/auxiliaries')
userSchema = require('../../schemas/user')

module.exports = broker.add({
    'submit #log-in form': (e, el) ->
        e.preventDefault() if e

        values = getFormValues(el)
        tasks.updateFormData(values)
        errors = tasks.validateForm(values, userSchema, ['name', 'password'])
        unless errors?.length
            values = parseFormValues(values)
            tasks.logInUser(values)
})
