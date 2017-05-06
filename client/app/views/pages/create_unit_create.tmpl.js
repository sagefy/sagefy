const {div, h1, a} = require('../../modules/tags')
const {unitWizard} = require('./create_shared.fn')
const {extend} = require('../../modules/utilities')
const unitSchema = require('../../schemas/unit')
const form = require('../components/form.tmpl')
const {createFieldsData} = require('../../modules/auxiliaries')
const icon = require('../components/icon.tmpl')

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
    description: 'Start with a verb, such as: "Compute the value of ' +
                 'dividing two whole numbers."',
    name: 'body'
}, {
    name: 'require_ids',
    label: 'Unit Requires',
    description: 'List the units required before this unit.',
    add: {
        url: '#',
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
    const proposedUnit = data.create && data.create.proposedUnit || {}

    const instanceFields = createFieldsData({
        schema: unitSchema,
        fields,
        errors: data.errors,
        formData: proposedUnit,
        sending: data.sending,
    })

    return div(
        {id: 'create', className: 'page create--unit-create'},
        h1('Create a New Unit for Subject'),
        unitWizard('list'),
        form(instanceFields),
        a(
            {href: '/create/unit/list'},
            icon('back'),
            ' Back to List of Units'
        )
    )
}
