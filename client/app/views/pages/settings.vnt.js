const broker = require('../../modules/broker')
const tasks = require('../../modules/tasks')
const {getFormValues, parseFormValues} = require('../../modules/auxiliaries')
const userSchema = require('../../schemas/user')

module.exports = broker.add({
    'submit #settings form'(e, el) {
        if (e) { e.preventDefault() }
        let values = getFormValues(el)
        tasks.updateFormData(values)
        const errors = tasks.validateForm(values, userSchema, ['name', 'email'])
        if(errors && errors.length) { return }
        values = parseFormValues(values)
        tasks.updateUser(values)
    }
})
