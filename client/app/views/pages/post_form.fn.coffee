# TODO add `available` field
# TODO how to decline proposal?
# TODO@ all proposal fields should lock after creating proposal
# TODO Tags (all)
# TODO@ Unit Belongs To (card only, should be provided by qs)

{extend} = require('../../modules/utilities')
{ucfirst, prefixObjectKeys} = require('../../modules/auxiliaries')

postSchema = require('../../schemas/post')
voteSchema = require('../../schemas/vote')
proposalSchema = require('../../schemas/proposal')

unitSchema = require('../../schemas/unit')
setSchema = require('../../schemas/set')
cardSchema = require('../../schemas/card')
videoCardSchema = require('../../schemas/cards/video_card')
choiceCardSchema = require('../../schemas/cards/choice_card')

schemas = {
    post: postSchema
    vote: voteSchema
    proposal: proposalSchema

    unit: unitSchema
    set: setSchema
    card: cardSchema
    videoCard: videoCardSchema
    choiceCard: choiceCardSchema
}

getFields = (formData) ->
    fields = []

    if formData['post.id']
        fields.push({
            name: 'post.id'
        })

    if formData['post.topic_id']
        fields.push({
            name: 'post.topic_id'
        })

    if formData['post.replies_to_id']
        fields.push({
            name: 'post.replies_to_id'
        })

    fields.push({
        name: 'post.kind'
        options: [{
            label: 'Post'
            disabled: !! formData['post.id']
        }, {
            label: 'Proposal'
            disabled: !! formData['post.id']
        }, {
            label: 'Vote'
            disabled: !! formData['post.id'] or \
                      not formData['post.replies_to_id']
        }]
        inline: true
        label: 'Post Kind'
    })

    if formData['post.kind'] is 'vote'
        fields.push({
            name: 'post.response'
            options: [
                {label: 'Yes, I agree'}
                {label: 'No, I dissent'}
            ]
            inline: true
            label: 'Response'
        })

    if formData['post.kind'] is 'proposal'
        fields.push({
            name: 'post.name'
            label: 'Proposal Name'
            description: 'Briefly state the goal of this proposal.'
        })

    fields.push({
        name: 'post.body'
        label: if formData['post.kind'] is 'proposal' \
               then 'Proposal Summary' \
               else 'Post Body'
        description: (if formData['post.kind'] is 'proposal' then \
                      'Describe the value of this proposal.'
                      else null)
    })

    if formData['post.kind'] is 'proposal'
        fields = fields.concat(getProposalFields(formData))

    return fields

getProposalFields = (formData) ->
    fields = []

    fields.push({
        name: 'post.entity_version.kind'
        label: 'Entity Kind'
        options: [
            {label: 'Card'}
            {label: 'Unit'}
            {label: 'Set'}
        ]
        inline: true
    })

    ###########################################################
    entityKind = formData['post.entity_version.kind']
    if not entityKind
        return fields

    if formData['entity.id']
        fields.push({
            name: 'entity.id'
        })

    fields.push({
        label: "#{ucfirst(entityKind)} Name"
        name: 'entity.name'
    })

    fields.push({
        label: "#{ucfirst(entityKind)} Language"
        name: 'entity.language'
        options: [
            {label: 'English'}
        ]
        value: 'en'
    })

    if entityKind in ['unit', 'set']
        fields.push({
            label: "#{ucfirst(entityKind)} Goal"
            description: 'Start with a verb, such as: Compute the value of ' +
                         'dividing two whole numbers.'
            name: 'entity.body'
        })

    if entityKind in ['card', 'unit']
        fields.push({
            name: 'entity.require_ids'
            label: "#{ucfirst(entityKind)} Requires"
            description: "List the #{entityKind}s required " +
                         "before this #{entityKind}."
        })

    if entityKind is 'set'
        fields.push({
            name: 'entity.members'
            label: 'Set Members'
            description: 'Choose a list of units and sets. ' +
                         'Cycles are not allowed.'
            columns: [
                {options: [
                    {label: 'Unit'}
                    {label: 'Set'}
                ]}
                {}
            ]
        })

    if entityKind is 'card'
        fields = fields.concat(getFieldsCardKind(formData))

    return fields

getFieldsCardKind = (formData) ->
    cardKind = formData['entity.kind']
    fields = []

    fields.push({
        label: 'Card Kind'
        name: 'entity.kind'
        options: [
            {label: 'Video'}
            {label: 'Choice'}
        ]
        inline: true
    })

    if cardKind is 'video'
        fields.push({
            label: 'Video Site'
            name: 'entity.site'
            options: [
                {label: 'YouTube'}
                {label: 'Vimeo'}
            ]
        })

        fields.push({
            label: 'Video ID'
            name: 'entity.video_id'
            description: 'You can find the video ID in the URL.'
        })

    if cardKind is 'choice'
        fields.push({
            label: 'Question or Prompt'
            name: 'entity.body'
        })

        fields.push({
            label: 'Response Options'
            name: 'entity.options'
            columns: [
                {options: [
                    {label: 'Yes'}
                    {label: 'No'}
                ]}
                {}
                {}
            ]
        })

        fields.push({
            label: 'Order'
            name: 'entity.order'
            options: [
                {label: 'Random'}
                {label: 'Set'}
            ]
        })

        fields.push({
            label: 'Max Options to Show'
            name: 'entity.max_options_to_show'
        })

    return fields

getSchema = (formData) ->
    schema = {}

    switch formData['post.kind']
        when 'proposal'
            extend(schema, prefixObjectKeys('post.', schemas.proposal))
        when 'vote'
            extend(schema, prefixObjectKeys('post.', schemas.vote))
        else
            extend(schema, prefixObjectKeys('post.', schemas.post))

    switch formData['post.entity_version.kind']
        when 'unit'
            extend(schema, prefixObjectKeys('entity.', schemas.unit))
        when 'set'
            extend(schema, prefixObjectKeys('entity.', schemas.set))
        when 'card'
            switch formData['entity.kind']
                when 'video'
                    extend(schema,
                           prefixObjectKeys('entity.', schemas.videoCard))
                when 'choice'
                    extend(schema,
                           prefixObjectKeys('entity.', schemas.choiceCard))
                else
                    extend(schema,
                           prefixObjectKeys('entity.', schemas.card))

    return schema

module.exports = {getFields, getSchema}
