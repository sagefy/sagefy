/*

const merge = require('lodash.merge')
const { div, h1, a, p } = require('../../helpers/tags')
const { cardWizard } = require('./create_shared.fn')
const cardSchema = require('../../schemas/card')
const videoCardSchema = require('../../schemas/cards/video_card')
const pageCardSchema = require('../../schemas/cards/page_card')
const unscoredEmbedCardSchema = require('../../schemas/cards/unscored_embed_card')
const choiceCardSchema = require('../../schemas/cards/choice_card')
const form = require('../components/form.tmpl')
const { createFieldsData, findGlobalErrors } = require('../../helpers/forms')
const icon = require('../components/icon.tmpl')
const { getIsLoggedIn } = require('../../selectors/base')
const spinner = require('../components/spinner.tmpl')
const goLogin = require('../../helpers/go_login')

const allKindsFields = [
  {
    label: 'Card Name',
    name: 'name',
  },
  {
    label: 'Card Language',
    name: 'language',
    options: [{ label: 'English' }],
    value: 'en',
  },
  {
    label: 'Card Kind',
    name: 'kind',
    options: [
      { label: 'Video' },
      { label: 'Choice' },
      { label: 'Page' },
      { label: 'Unscored Embed' },
    ],
    inline: true,
  },
]

/* {
   name: 'require_ids',
   label: 'Card Requires',
   description: 'List the cards required before this card.',
}, /

const videoFields = allKindsFields.concat([
  {
    label: 'Video Site',
    name: 'data.site',
    options: [{ label: 'YouTube' }, { label: 'Vimeo' }],
  },
  {
    label: 'Video ID',
    name: 'data.video_id',
    description:
      'You can find the video ID in the URL. Look for https://www.youtube.com/watch?v=VIDEO_ID_HERE',
  },
  {
    type: 'submit',
    name: 'submit',
    label: 'Create Video Card',
    icon: 'create',
  },
])

const pageFields = allKindsFields.concat([
  {
    label: 'Body',
    name: 'data.body',
    description: 'Format with: _ ** # ![]().',
  },
  {
    type: 'submit',
    name: 'submit',
    label: 'Create Page Card',
    icon: 'create',
  },
])

const unscoredEmbedFields = allKindsFields.concat([
  {
    label: 'URL',
    name: 'data.url',
    description: 'Use `https`. Full URL.',
  },
  {
    type: 'submit',
    name: 'submit',
    label: 'Create Unscored Embed Card',
    icon: 'create',
  },
])

const choiceFields = allKindsFields.concat([
  {
    label: 'Question or Prompt',
    name: 'data.body',
  },
  {
    label: 'Response Options',
    name: 'data.options',
    columns: [
      {
        options: [{ label: 'Yes' }, { label: 'No' }],
      },
      {},
      {},
    ],
  },
  {
    label: 'Order',
    name: 'data.order',
    options: [{ label: 'Random' }, { label: 'Set' }],
  },
  {
    label: 'Max Options to Show',
    name: 'data.max_options_to_show',
  },
  {
    type: 'submit',
    name: 'submit',
    label: 'Create Choice Card',
    icon: 'create',
  },
])

allKindsFields.forEach((field, index) => {
  allKindsFields[index] = merge({}, allKindsFields[field.name] || {}, field)
})

videoFields.forEach((field, index) => {
  videoFields[index] = merge({}, videoFields[field.name] || {}, field)
})

pageFields.forEach((field, index) => {
  pageFields[index] = merge({}, pageFields[field.name] || {}, field)
})

unscoredEmbedFields.forEach((field, index) => {
  unscoredEmbedFields[index] = merge(
    {},
    unscoredEmbedFields[field.name] || {},
    field
  )
})

choiceFields.forEach((field, index) => {
  choiceFields[index] = merge({}, choiceFields[field.name] || {}, field)
})

module.exports = function createCardCreate(data) {
  if (getIsLoggedIn(data) === null) {
    return spinner()
  }

  if (!getIsLoggedIn(data)) {
    return goLogin()
  }

  const proposedCard = (data.create && data.create.proposedCard) || {}
  const cardKind = proposedCard.kind
  const fields =
    {
      video: videoFields,
      page: pageFields,
      unscored_embed: unscoredEmbedFields,
      choice: choiceFields,
    }[cardKind] || allKindsFields
  const schema =
    {
      video: videoCardSchema,
      page: pageCardSchema,
      unscored_embed: unscoredEmbedCardSchema,
      choice: choiceCardSchema,
    }[cardKind] || cardSchema
  const instanceFields = createFieldsData({
    schema,
    fields,
    errors: data.errors,
    formData: proposedCard,
    sending: data.sending,
  })
  const globalErrors = findGlobalErrors({
    fields,
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
    p(
      'After you submit here, "Submit These Cards" on the list page to finish.'
    ),
    a(
      { href: '/create/card/list' },
      icon('back'),
      ' Cancel & Back to List of Cards'
    )
  )
}
*/
