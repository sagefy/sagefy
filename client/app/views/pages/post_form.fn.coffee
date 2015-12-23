{extend} = require('../../modules/utilities')
postSchema = require('../../schemas/post')
voteSchema = require('../../schemas/vote')
proposalSchema = require('../../schemas/proposal')
unitSchema = require('../../schemas/unit')

schemas = {
    post: postSchema
    vote: voteSchema
    proposal: proposalSchema
    unit: unitSchema
}

getFields = ({topicID, repliesToID, editKind, postKind = 'post'}) ->
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
            # Post
            disabled: not editKind
        }, {
            # Proposal
            disabled: not editKind
        }, {
            # Vote
            disabled: not (editKind and repliesToID)
        }, {
            # Flag
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
        fields = fields.concat(getProposalFields())

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

getProposalFields = (entityKind) ->
    # TODO all proposal fields should lock after creating proposal

    fields = []

    fields.push(extend({
        label: 'Entity Kind'
        options: [
            {label: 'Card'}
            {label: 'Unit'}
            {label: 'Set'}
        ]
        inline: true
        name: 'entity.kind'
    }, schemas.proposal['entity.kind']))

    # TODO Entity ID not on create entity
    fields.push(extend({

    }, schemas.proposal['entity.id']))

    ###########################################################
    if not entityKind
        return fields

    fields.push(extend({
        label: 'Entity Name'
    }, schemas[entityKind].name))

    fields.push(extend({
        label: 'Entity Language'
        options: [
            {label: 'English'}
        ]
        value: 'en'
    }, schemas[entityKind].language))

    # TODO Tags (all)

    if entityKind in ['unit', 'set']
        fields.push(extend({
            label: 'Entity Goal'
            description: 'Start with a verb, such as: Compute the value of ' +
                         'dividing two whole numbers.'
        }, schemas[entityKind].body))

    # Unit Belongs To (card only, should be provided by qs)

    # TODO input method for requires?
    if entityKind in ['card', 'unit']
        fields.push(extend({
            label: 'Entity Requires'
            description: "List the #{entityKind}s required " +
                         "before this #{entityKind}."
        }, schemas[entityKind].requires))

    # Members [id, kind] (set)
    # Card Kind (card)
    # Video Site (video card)
    # Video ID (video card)
    # Choice Question [Body] (choice card)
    # Choice Options [value, correct, feedback] (choice card)
    # Choice Feedback (choice card)
    # Choice Order (choice card)
    # Choice Max Options to Show (choice card)
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
