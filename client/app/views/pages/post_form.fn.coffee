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
        label: 'Kind'
    }, schemas[postKind].kind))

    if postKind is 'vote'
        fields.push(extend({
            name: 'post.response'
            options: [
                {label: 'Yes, I agree'}
                {label: 'No, I dissent'}
            ]
            inline: true
            label: 'Response'
        }, schemas[postKind].response))

    fields.push(extend({
        name: 'post.body'
        label: 'Body'
    }, schemas[postKind].body))

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
