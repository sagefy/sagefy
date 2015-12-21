postSchema = require('../../schemas/post')
{extend} = require('../../modules/utilities')

getFields = ({topicID, postID, repliesToID}) ->
    return [extend({
        name: 'post.topic_id'
        value: topicID
    }, postSchema.topic_id), extend({
        name: 'post.replies_to_id'
        value: repliesToID
    }, postSchema.replies_to_id), extend({
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
    }, postSchema.body)]

parseData = (data) ->
    [topicID, postID] = data.routeArgs
    repliesToID = data.routeQuery.replies_to_id
    if postID
        post = data.topicPosts?[topicID].find((post) -> post.id is postID)
    if post
        formData = {
            'post.replies_to_id': post.replies_to_id
            'post.kind': post.kind
            'post.body': post.body
        }
    else
        formData = {}

    return {topicID, postID, repliesToID, post, formData}

module.exports = {getFields, parseData}
