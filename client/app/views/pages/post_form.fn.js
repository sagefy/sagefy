// TODO-2 add `available` field
// TODO-2 on update: how to decline a proposal?
// TODO-3 Tags (all)

const {extend} = require('../../modules/utilities')
const {ucfirst, prefixObjectKeys} = require('../../modules/auxiliaries')

const postSchema = require('../../schemas/post')
const voteSchema = require('../../schemas/vote')
const proposalSchema = require('../../schemas/proposal')

const unitSchema = require('../../schemas/unit')
const setSchema = require('../../schemas/set')
const cardSchema = require('../../schemas/card')
const videoCardSchema = require('../../schemas/cards/video_card')
const choiceCardSchema = require('../../schemas/cards/choice_card')

const schemas = {
    post: postSchema,
    vote: voteSchema,
    proposal: proposalSchema,

    unit: unitSchema,
    set: setSchema,
    card: cardSchema,
    videoCard: videoCardSchema,
    choiceCard: choiceCardSchema,
}

const getFields = (formData) => {
    let fields = []

    ;[
        'post.id',
        'post.topic_id',
        'post.replies_to_id',
    ].forEach((name) => {
        if (formData[name]) { fields.push({name}) }
    })

    fields.push({
        name: 'post.kind',
        options: [{
            label: 'Post',
            disabled: !! formData['post.id'],
        }, {
            label: 'Proposal',
            disabled: !! formData['post.id'],
        }, {
            label: 'Vote',
            disabled: !! formData['post.id'] ||
                      ! formData['post.replies_to_id']
        }],
        inline: true,
        label: 'Post Kind'
    })

    if (formData['post.kind'] === 'vote') {
        fields.push({
            name: 'post.response',
            options: [
                {label: 'Yes, I agree'},
                {label: 'No, I dissent'}
            ],
            inline: true,
            label: 'Response',
            disabled: !! formData['post.id']
        })
    }

    if (formData['post.kind'] === 'proposal') {
        fields.push({
            name: 'post.name',
            label: 'Proposal Name',
            description: 'Briefly state the goal of this proposal.'
        })
    }

    fields.push({
        name: 'post.body',
        label: formData['post.kind'] === 'proposal' ?
               'Proposal Summary' :
               'Post Body',
        description: (formData['post.kind'] === 'proposal' ?
                      'Describe the value of this proposal.'
                      : null)
    })

    if (formData['post.kind'] === 'proposal' && ! formData['post.id']) {
        fields = fields.concat(getProposalFields(formData))
    }

    return fields
}

const getProposalFields = (formData) => {
    let fields = []

    fields.push({
        name: 'post.entity_version.kind',
        label: 'Entity Kind',
        options: [
            {label: 'Card'},
            {label: 'Unit'},
            {label: 'Set'},
        ],
        inline: true
    })

    // ##########################################################
    const entityKind = formData['post.entity_version.kind']
    if (! entityKind) { return fields }
    if (formData['entity.id']) {
        fields.push({
            name: 'entity.id'
        })
    }
    fields.push({
        label: `${ucfirst(entityKind)} Name`,
        name: 'entity.name',
    })
    fields.push({
        label: `${ucfirst(entityKind)} Language`,
        name: 'entity.language',
        options: [
            {label: 'English'}
        ],
        value: 'en'
    })
    if (entityKind === 'card') {
        fields.push({
            name: 'entity.unit_id',
            label: 'Card\'s Unit ID',
            description: 'Add the ID of the unit the card belongs to. ' +
                         'You can find this in the URL of the unit.'
        })
    }
    if (['unit', 'set'].indexOf(entityKind) > -1) {
        fields.push({
            label: `${ucfirst(entityKind)} Goal`,
            description: 'Start with a verb, such as: Compute the value of ' +
                         'dividing two whole numbers.',
            name: 'entity.body'
        })
    }
    if (['card', 'unit'].indexOf(entityKind) > -1) {
        fields.push({
            name: 'entity.require_ids',
            label: `${ucfirst(entityKind)} Requires`,
            description: `List the ${entityKind}s required ` +
                         `before this ${entityKind}.`
        })
    }
    if (entityKind === 'set') {
        fields.push({
            name: 'entity.members',
            label: 'Set Members',
            description: 'Choose a list of units and sets. ' +
                         'Cycles are not allowed.',
            columns: [
                {options: [
                    {label: 'Unit'},
                    {label: 'Set'}
                ]},
                {}
            ]
        })
    }
    if (entityKind === 'card') {
        fields = fields.concat(getFieldsCardKind(formData))
    }
    return fields
}

const getFieldsCardKind = (formData) => {
    const cardKind = formData['entity.kind']
    const fields = []

    fields.push({
        label: 'Card Kind',
        name: 'entity.kind',
        options: [
            {label: 'Video'},
            {label: 'Choice'}
        ],
        inline: true
    })

    if (cardKind === 'video') {
        fields.push({
            label: 'Video Site',
            name: 'entity.site',
            options: [
                {label: 'YouTube'},
                {label: 'Vimeo'}
            ]
        })

        fields.push({
            label: 'Video ID',
            name: 'entity.video_id',
            description: 'You can find the video ID in the URL.'
        })
    }

    if (cardKind === 'choice') {
        fields.push({
            label: 'Question or Prompt',
            name: 'entity.body',
        })

        fields.push({
            label: 'Response Options',
            name: 'entity.options',
            columns: [
                {options: [
                    {label: 'Yes'},
                    {label: 'No'},
                ]},
                {},
                {}
            ]
        })

        fields.push({
            label: 'Order',
            name: 'entity.order',
            options: [
                {label: 'Random'},
                {label: 'Set'}
            ]
        })

        fields.push({
            label: 'Max Options to Show',
            name: 'entity.max_options_to_show'
        })
    }

    return fields
}

const getSchema = (formData) => {
    const schema = {}

    if (formData['post.kind'] === 'proposal') {
        extend(schema, prefixObjectKeys('post.', schemas.proposal))
    } else if (formData['post.kind'] === 'vote') {
        extend(schema, prefixObjectKeys('post.', schemas.vote))
    } else {
        extend(schema, prefixObjectKeys('post.', schemas.post))
    }

    if (formData['post.entity_version.kind'] === 'unit') {
        extend(schema, prefixObjectKeys('entity.', schemas.unit))
    } else if (formData['post.entity_version.kind'] === 'set') {
        extend(schema, prefixObjectKeys('entity.', schemas.set))
    } else if (formData['post.entity_version.kind'] === 'card') {
        if (formData['entity.kind'] === 'video') {
            extend(schema,
                   prefixObjectKeys('entity.', schemas.videoCard))
        } else if (formData['entity.kind'] === 'choice') {
            extend(schema,
                   prefixObjectKeys('entity.', schemas.choiceCard))
        } else {
            extend(schema,
                   prefixObjectKeys('entity.', schemas.card))
        }
    }

    return schema
}

module.exports = {getFields, getSchema}
