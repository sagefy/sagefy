{extend} = require('../../modules/utilities')
postSchema = require('../../schemas/post')
voteSchema = require('../../schemas/vote')
proposalSchema = require('../../schemas/proposal')

schemas = {
    post: postSchema
    vote: voteSchema
    proposal: proposalSchema
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
        label: 'Post Body'
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
        label: 'Post Name'
    }, schemas.proposal.name)

getProposalFields = () ->
    # TODO all proposal fields should lock after creating proposal
    # Entity Kind (all)
    # Entity ID (all, not on create entity)
    # Entity Name (all)
    # Entity Language (en only option)
    # Entity Body (unit or set)
    # Unit Belongs To (card only, should be provided by qs)
    # Tags (all)
    # Requires (card or unit)
    # Members [id, kind] (set)
    # Card Kind (card)
    # Video Site (video card)
    # Video ID (video card)
    # Choice Question [Body] (choice card)
    # Choice Options [value, correct, feedback] (choice card)
    # Choice Feedback (choice card)
    # Choice Order (choice card)
    # Choice Max Options to Show (choice card)
    return []

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
