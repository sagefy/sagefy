const broker = require('../../modules/broker')
const tasks = require('../../modules/tasks')
const {getFormValues, parseFormValues} =
    require('../../modules/auxiliaries')
const setSchema = require('../../schemas/set')
const {closest} = require('../../modules/utilities')

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
        values = parseFormValues(values)
        const errors = tasks.validateForm(values, setSchema,
            ['name', 'language', 'body', 'members'])
        if(errors && errors.length) { return }
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
            }],
        }
        tasks.createSetProposal(data)
    },

    'submit .create--set-add__form'(e, el) {
        if(e) e.preventDefault()
        const q = el.querySelector('input').value
        tasks.search({ q, kind: 'unit,set' })
    },

    'click .create--set-add__add'(e, el) {
        if(e) e.preventDefault()
        const {kind, id, name, body} = el.dataset
        tasks.addMemberToCreateSet({kind, id, name, body})
    },

    'click .create--set-create .form-field--entities__a'(e, el) {
        if(e) e.preventDefault()
        const form = closest(el, 'form')
        const values = getFormValues(form)
        tasks.createSetData(values)
    },

    'click .create--set-create .form-field--entities__remove'(e, el) {
        if(e) e.preventDefault()
        const id = el.id
        tasks.removeMemberFromCreateSet({id})
    },

    'click .create--unit-find__choose'(e, el) {
        if(e) e.preventDefault()
        const {id, name} = el.dataset
        tasks.createChooseSetForUnits({id, name})
    },

    'submit .create--unit-find__form'(e, el) {
        if(e) e.preventDefault()
        const q = el.querySelector('input').value
        tasks.search({ q, kind: 'set' })
    },

    'click .create--unit-list__remove'(e, el) {
        if(e) e.preventDefault()
    },

    'click .create--unit-list__create'(e, el) {
        if(e) e.preventDefault()
    },

    'click .create--unit-list__add'(e, el) {
        if(e) e.preventDefault()
    },

    'click .create--unit-list__submit'(e, el) {
        if(e) e.preventDefault()
    },
})
