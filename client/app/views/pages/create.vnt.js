const broker = require('../../modules/broker')
const tasks = require('../../modules/tasks')
const {getFormValues, parseFormValues} =
    require('../../modules/auxiliaries')
const setSchema = require('../../schemas/set')

module.exports = broker.add({
    'click .create__route': (e, el) => {
        if(e) e.preventDefault()
        const [,, kind, step] = el.pathname.split('/')
        tasks.resetCreate()
        tasks.updateCreateRoute({kind, step})
    },

    'submit .create--set-create form': (e, el) => {
        if(e) e.preventDefault()
        let values = getFormValues(el)
        tasks.updateFormData(values)
        const errors = tasks.validateForm(values, setSchema,
            ['name', 'language', 'body'])  // TODO members
        if(errors && errors.length) { return }
        values = parseFormValues(values)
        tasks.wantCreateSet(values) // TODO go ahead and make the network call
    }
})
