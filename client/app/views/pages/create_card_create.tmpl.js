const { div, h1, a, p } = require('../../modules/tags')
const { cardWizard } = require('./create_shared.fn')
const { extend } = require('../../modules/utilities')
const cardSchema = require('../../schemas/card')
const videoCardSchema = require('../../schemas/cards/video_card')
const choiceCardSchema = require('../../schemas/cards/choice_card')
const form = require('../components/form.tmpl')
const { createFieldsData, findGlobalErrors } = require('../../modules/auxiliaries')
const icon = require('../components/icon.tmpl')

const allKindsFields = [{
    label: 'Card Name',
    name: 'name',
}, {
    label: 'Card Language',
    name: 'language',
    options: [
        { label: 'English' },
    ],
    value: 'en',
}, {
    label: 'Card Kind',
    name: 'kind',
    options: [
        { label: 'Video' },
        { label: 'Choice' },
    ],
    inline: true,
}]

/* {
   name: 'require_ids',
   label: 'Card Requires',
   description: 'List the cards required before this card.',
}, */

const videoFields = allKindsFields.concat([{
    label: 'Video Site',
    name: 'site',
    options: [
        { label: 'YouTube' },
        { label: 'Vimeo' },
    ],
}, {
    label: 'Video ID',
    name: 'video_id',
    description: 'You can find the video ID in the URL. Look for https://www.youtube.com/watch?v=VIDEO_ID_HERE',
}, {
    type: 'submit',
    name: 'submit',
    label: 'Create Video Card',
    icon: 'create',
}])

const choiceFields = allKindsFields.concat([{
    label: 'Question or Prompt',
    name: 'body',
}, {
    label: 'Response Options',
    name: 'options',
    columns: [
        { options: [
            { label: 'Yes' },
            { label: 'No' },
        ] },
        {},
        {},
    ],
}, {
    label: 'Order',
    name: 'order',
    options: [
        { label: 'Random' },
        { label: 'Set' },
    ],
}, {
    label: 'Max Options to Show',
    name: 'max_options_to_show',
}, {
    type: 'submit',
    name: 'submit',
    label: 'Create Choice Card',
    icon: 'create',
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
    const proposedCard = data.create && data.create.proposedCard || {}
    const cardKind = proposedCard.kind

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
        formData: proposedCard,
        sending: data.sending,
    })

    const globalErrors = findGlobalErrors({
        fields: fields,
        errors: data.errors,
    })

    return div(
        { id: 'create', className: 'page create--card-create' },
        h1('Create a New Card for Unit'),
        cardWizard('list'),
        form({
            fields: instanceFields,
            errors: globalErrors,
        }),
        p('After you submit here, "Submit These Cards" on the list page to finish.'),
        a(
            { href: '/create/card/list' },
            icon('back'),
            ' Cancel & Back to List of Cards'
        )
    )
}
