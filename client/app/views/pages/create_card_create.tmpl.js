const {div, h1} = require('../../modules/tags')
const {cardWizard} = require('./create_shared.fn')
const {extend} = require('../../modules/utilities')
const cardSchema = require('../../schemas/card')
const videoCardSchema = require('../../schemas/cards/video_card')
const choiceCardSchema = require('../../schemas/cards/choice_card')
const form = require('../components/form.tmpl')
const {createFieldsData} = require('../../modules/auxiliaries')

const allKindsFields = [{
    label: 'Card Name',
    name: 'name',
}, {
    label: 'Card Language',
    name: 'language',
    options: [
        {label: 'English'}
    ],
    value: 'en'
}, {
    name: 'unit_id',
    label: 'Card\'s Unit ID',
    description: 'Add the ID of the unit the card belongs to. ' +
                 'You can find this in the URL of the unit.'
}, {
    name: 'require_ids',
    label: 'Card Requires',
    description: 'List the cards required before this card.',
}, {
    label: 'Card Kind',
    name: 'kind',
    options: [
        {label: 'Video'},
        {label: 'Choice'}
    ],
    inline: true
}]

const videoFields = allKindsFields.concat([{
    label: 'Video Site',
    name: 'site',
    options: [
        {label: 'YouTube'},
        {label: 'Vimeo'},
    ],
}, {
    label: 'Video ID',
    name: 'video_id',
    description: 'You can find the video ID in the URL.',
}, {
    type: 'submit',
    name: 'submit',
    label: 'Create Video Card',
    icon: 'create'
}])

const choiceFields = allKindsFields.concat([{
    label: 'Question or Prompt',
    name: 'body',
}, {
    label: 'Response Options',
    name: 'options',
    columns: [
        {options: [
            {label: 'Yes'},
            {label: 'No'},
        ]},
        {},
        {}
    ]
}, {
    label: 'Order',
    name: 'order',
    options: [
        {label: 'Random'},
        {label: 'Set'}
    ]
}, {
    label: 'Max Options to Show',
    name: 'max_options_to_show'
}, {
    type: 'submit',
    name: 'submit',
    label: 'Create Choice Card',
    icon: 'create'
}])

allKindsFields.forEach((field, index) => {
    allKindsFields[index] = extend({}, allKindsFields[field.name] || {}, field)
})

videoFields.forEach((field, index) => {
    videoFields[index] = extend({}, videoFields[field.name] || {}, field)
})

choiceFields.forEach((field, index) => {
    choiceFields[index] = extend({}, choiceFields[field.name] || {}, field)
})

module.exports = function createCardCreate(data) {
    const cardKind = 'video' // TODO-0 update this to use value

    const fields = cardKind === 'video' ? videoFields
        : cardKind === 'choice' ? choiceFields
        : allKindsFields

    const schema = cardKind === 'video' ? videoCardSchema
        : cardKind === 'choice' ? choiceCardSchema
        : cardSchema

    const instanceFields = createFieldsData({
        schema,
        fields,
        errors: data.errors,
        formData: data.formData,
        sending: data.sending,
    })

    return div(
        {id: 'create', className: 'page'},
        h1('Create a New Card for Unit'),
        cardWizard('list'),
        form(instanceFields)
    )
}
