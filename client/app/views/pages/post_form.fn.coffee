postSchema = require('../../schemas/post')
{extend} = require('../../modules/utilities')

getFields = ({topicID, repliesToID}) ->
    fields = []

    if topicID
        fields.push(extend({
            name: 'post.topic_id'
            value: topicID
        }, postSchema.topic_id))

    if repliesToID
        fields.push(extend({
            name: 'post.replies_to_id'
            value: repliesToID
        }, postSchema.replies_to_id))

    fields.push(extend({
        name: 'post.kind'
        options: [{

        }, {
            disabled: true
        }, {
            disabled: true
        }, {
            disabled: true
        }]
        inline: true
        label: 'Kind'
    }, postSchema.kind), extend({
        name: 'post.body'
        label: 'Body'
    }, postSchema.body))

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
    } else {}

    return {topicID, postID, repliesToID, post, formData}

module.exports = {getFields, parseData}
