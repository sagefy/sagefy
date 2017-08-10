const { div, h1 } = require('../../modules/tags')
const { extend } = require('../../modules/utilities')
const subjectSchema = require('../../schemas/subject')
const form = require('../components/form.tmpl')
const {
    createFieldsData,
    findGlobalErrors,
} = require('../../modules/auxiliaries')

const fields = [
    {
        label: 'Subject Name',
        name: 'name',
    },
    {
        label: 'Subject Language',
        name: 'language',
        options: [{ label: 'English' }],
        value: 'en',
    },
    {
        label: 'Subject Goal',
        description:
            'Start with a verb, such as: Compute the value of ' +
            'dividing two whole numbers.',
        name: 'body',
    },
    {
        name: 'members',
        label: 'Subject Members',
        description:
            'Choose a list of units and subjects. '
            + 'Cycles are not allowed.',
        add: {
            label: 'Add an Existing Unit or Subject',
            url: '#',
        },
    },
    {
        type: 'submit',
        name: 'submit',
        label: 'Create Subject',
        icon: 'create',
    },
]

fields.forEach((field, index) => {
    fields[index] = extend({}, subjectSchema[field.name] || {}, field)
})

module.exports = function createSubjectCreate(data) {
    const instanceFields = createFieldsData({
        schema: subjectSchema,
        fields,
        errors: data.errors,
        formData: data.create.subject || {},
        sending: data.sending,
    })

    const globalErrors = findGlobalErrors({
        fields: fields,
        errors: data.errors,
    })

    return div(
        { id: 'create', className: 'page create--subject-create' },
        h1('Create a New Subject'),
        form({
            fields: instanceFields,
            errors: globalErrors,
        })
    )
}
