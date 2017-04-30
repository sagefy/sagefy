const {div, h1} = require('../../modules/tags')
const {unitWizard} = require('./create_shared.fn')
const {extend} = require('../../modules/utilities')
const unitSchema = require('../../schemas/set')
const form = require('../components/form.tmpl')
const {createFieldsData} = require('../../modules/auxiliaries')

const fields = [{
    label: 'Unit Name',
    name: 'name',
}, {
    label: 'Unit Language',
    name: 'language',
    options: [
        {label: 'English'}
    ],
    value: 'en'
}, {
    label: 'Unit Goal',
    description: 'Start with a verb, such as: Compute the value of ' +
                 'dividing two whole numbers.',
    name: 'body'
}, {
    name: 'require_ids',
    label: 'Unit Requires',
    description: 'List the units required before this unit.',
    add: {
        url: '/create/unit/???',
        label: 'Find a Unit to Require',
    },
}, {
    type: 'submit',
    name: 'submit',
    label: 'Create Unit',
    icon: 'create'
}]

fields.forEach((field, index) => {
    fields[index] = extend({}, unitSchema[field.name] || {}, field)
})

module.exports = function createUnitCreate(data) {
    const instanceFields = createFieldsData({
        schema: unitSchema,
        fields,
        errors: data.errors,
        formData: data.formData,
        sending: data.sending,
    })

    return div(
        {id: 'create', className: 'page'},
        h1('Create a New Unit for Set'),
        unitWizard('list'),
        form(instanceFields)
        // Back to list view button
    )
}
