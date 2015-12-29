
###
TODO@ modes:
          topic    post
create ------------------
- card    [ ]      [ ]
- unit    [ ]      [ ]
- set     [ ]      [ ]
update (view only) ------
- card    -x-      [ ]   - TODO@ how to decline proposal?
- unit    -x-      [ ]
- set     -x-      [ ]
###

{extend} = require('../../modules/utilities')
{ucfirst} = require('../../modules/auxiliaries')
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

getFields = ({
    topicID
    repliesToID
    editKind
    postKind = 'post'
    entityKind
    cardKind
}) ->
    fields = []

    if topicID
        fields.push(extend({
            name: 'post.topic_id'
            value: topicID
        }, schemas[postKind].topic_id))

    if repliesToID
        fields.push(extend({
            name: 'post.replies_to_id'
            value: repliesToID
        }, schemas[postKind].replies_to_id))

    fields.push(extend({
        name: 'post.kind'
        options: [{
            label: 'Post'
            disabled: not editKind
        }, {
            label: 'Proposal'
            disabled: not editKind
        }, {
            label: 'Vote'
            disabled: not (editKind and repliesToID)
        }, {
            label: 'Flag'
            disabled: true
        }]
        inline: true
        label: 'Post Kind'
    }, schemas[postKind].kind))

    if postKind is 'vote'
        fields.push(getFieldsVote())

    if postKind is 'proposal'
        fields.push(getProposalName())

    fields.push(extend({
        name: 'post.body'
        label: if postKind is 'proposal' \
               then 'Proposal Summary' \
               else 'Post Body'
        description: (if postKind is 'proposal' then \
                      'Describe the value of this proposal.'
                      else null)
    }, schemas[postKind].body))

    if postKind is 'proposal'
        fields = fields.concat(getProposalFields(entityKind, cardKind))

    return fields

getFieldsVote = () ->
    return extend({
        name: 'post.response'
        options: [
            {label: 'Yes, I agree'}
            {label: 'No, I dissent'}
        ]
        inline: true
        label: 'Response'
    }, schemas.vote.response)

getProposalName = () ->
    return extend({
        name: 'post.name'
        label: 'Proposal Name'
        description: 'Briefly state the goal of this proposal.'
    }, schemas.proposal.name)

getProposalFields = (entityKind, cardKind) ->
    # TODO@ all proposal fields should lock after creating proposal

    fields = []

    fields.push(extend({
        label: 'Entity Kind'
        options: [
            {label: 'Card'}
            {label: 'Unit'}
            {label: 'Set'}
        ]
        inline: true
        name: 'entity_kind'  # We rename to avoid conflict with card kind
    }, schemas.proposal['entity.kind']))

    # TODO@ Entity ID not on create entity
    fields.push(extend({

    }, schemas.proposal['entity.id']))

    ###########################################################
    if not entityKind
        return fields

    fields.push(extend({
        label: "#{ucfirst(entityKind)} Name"
    }, schemas[entityKind].name))

    fields.push(extend({
        label: "#{ucfirst(entityKind)} Language"
        options: [
            {label: 'English'}
        ]
        value: 'en'
    }, schemas[entityKind].language))

    # TODO Tags (all)

    if entityKind in ['unit', 'set']
        fields.push(extend({
            label: "#{ucfirst(entityKind)} Goal"
            description: 'Start with a verb, such as: Compute the value of ' +
                         'dividing two whole numbers.'
        }, schemas[entityKind].body))

    # TODO@ Unit Belongs To (card only, should be provided by qs)

    if entityKind in ['card', 'unit']
        fields.push(extend({
            name: 'entity.require_ids'
            label: "#{ucfirst(entityKind)} Requires"
            description: "List the #{entityKind}s required " +
                         "before this #{entityKind}."
        }, schemas[entityKind].require_ids))

    if entityKind is 'set'
        fields.push(extend({
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
        }, schemas.set.members))


    if entityKind is 'card'
        fields = fields.concat(getFieldsCardKind(cardKind))

    return fields

getFieldsCardKind = (cardKind) ->
    fields = []

    fields.push(extend({
        label: 'Card Kind'
        name: 'entity.kind'
        options: [
            {label: 'Video'}
            {label: 'Choice'}
        ]
        inline: true
    }, schemas.card.kind))

    if cardKind is 'video'
        fields.push(extend({
            label: 'Video Site'
            name: 'entity.site'
            options: [
                {label: 'YouTube'}
                {label: 'Vimeo'}
            ]
        }, schemas.videoCard.site))

        fields.push(extend({
            label: 'Video ID'
            name: 'entity.video_id'
            description: 'You can find the video ID in the URL.'
        }, schemas.videoCard.video_id))

    if cardKind is 'choice'
        fields.push(extend({
            label: 'Question or Prompt'
            name: 'entity.body'
        }, schemas.choiceCard.body))

        fields.push(extend({
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
        }, schemas.choiceCard.options))

        fields.push(extend({
            label: 'Order'
            name: 'entity.order'
            options: [
                {label: 'Random'}
                {label: 'Set'}
            ]
        }, schemas.choiceCard.order))

        fields.push(extend({
            label: 'Max Options to Show'
            name: 'entity.max_options_to_show'
        }, schemas.choiceCard.max_options_to_show))

    return fields

parseData = (data) ->
    [topicID, postID] = data.routeArgs

    if postID
        post = data.topicPosts?[topicID].find((post) -> post.id is postID)

    repliesToID = if post then post.replies_to_id \
                  else data.routeQuery.replies_to_id

    formData = if post then {
        'post.replies_to_id': repliesToID
        'post.kind': post.kind
        'post.body': post.body
        'post.response': '' + post.response
    } else {}

    return {topicID, postID, repliesToID, post, formData}

module.exports = {getFields, parseData}
