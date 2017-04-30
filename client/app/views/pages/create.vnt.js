const broker = require('../../modules/broker')
const tasks = require('../../modules/tasks')
const {getFormValues, parseFormValues} =
    require('../../modules/auxiliaries')
const setSchema = require('../../schemas/set')

module.exports = broker.add({
    'click .create__route'(e, el) {
        if(e) e.preventDefault()
        const [,, kind, step] = el.pathname.split('/')
        tasks.resetCreate()
        tasks.updateCreateRoute({kind, step})
    },

    'submit .create--set-create form'(e, el) {
        if(e) e.preventDefault()
        let values = getFormValues(el)
        tasks.updateFormData(values)
        const errors = tasks.validateForm(values, setSchema,
            ['name', 'language', 'body'])  // TODO members
        if(errors && errors.length) { return }
        values = parseFormValues(values)
        const data = {
            topic: {
                name: `Create a Set: ${values.name}`,
                entity: {
                    id: '1rk0jS5EGEavSG4NBxRvPkZf',
                    kind: 'unit',
                }
            },
            post: {
                kind: 'proposal',
                body: `Create a Set: ${values.name}`,
            },
            sets: [{
                name: values.name,
                body: values.body,
                members: values.members,
                /* members: [{
                    id
                    kind
                }] */
            }],
        }
        tasks.createSetProposal(data)
    },

    'submit .create--set-add__form'(e, el) {
        if(e) e.preventDefault()
        const q = el.querySelector('input').value
        tasks.search({ q, kind: 'unit,set' })
    },

    /* 'click .create--set-add__add'(e, el) {
        if(e) e.preventDefault()
    } */
})
