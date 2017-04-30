const {div, h1} = require('../../modules/tags')
const {extend} = require('../../modules/utilities')
const setSchema = require('../../schemas/set')
const form = require('../components/form.tmpl')
const {createFieldsData} = require('../../modules/auxiliaries')

const fields = [{
    label: 'Set Name',
    name: 'name',
}, {
    label: 'Set Language',
    name: 'language',
    options: [
        {label: 'English'}
    ],
    value: 'en'
}, {
    label: 'Set Goal',
    description: 'Start with a verb, such as: Compute the value of ' +
                 'dividing two whole numbers.',
    name: 'body'
}, {
    name: 'members',
    label: 'Set Members',
    description: 'Choose a list of units and sets. ' +
                 'Cycles are not allowed.',
    add: {
        label: 'Add an Existing Unit or Set',
        url: '/create/set/add',
    }
}, {
    type: 'submit',
    name: 'submit',
    label: 'Create Set',
    icon: 'create'
}]

fields.forEach((field, index) => {
    fields[index] = extend({}, setSchema[field.name] || {}, field)
})

module.exports = function createSetCreate(data) {
    const instanceFields = createFieldsData({
        schema: setSchema,
        fields,
        errors: data.errors,
        formData: data.create.set || {},
        sending: data.sending,
    })

    return div(
        {id: 'create', className: 'page create--set-create'},
        h1('Create a New Set'),
        form(instanceFields)
    )
}
