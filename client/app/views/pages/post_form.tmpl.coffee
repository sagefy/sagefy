{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get
form = require('../components/form.tmpl')
postSchema = require('../../schemas/post')
{extend} = require('../../modules/utilities')
{mergeFieldsData} = require('../../modules/auxiliaries')

getFields = (topicID, postID, data) ->
    fields = [extend({
        name: 'post.topic_id'
        value: topicID
    }, postSchema.topic_id), extend({
        name: 'post.replies_to_id'
        value: data.routeQuery.replies_to_id
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
    }, postSchema.body), {
        id: postID
        type: 'submit'
        name: 'submit'
        label: if postID then 'Update Post' else 'Create Post'
        icon: 'plus'
    }]

    return fields

module.exports = (data) ->
    [topicID, postID] = data.routeArgs
    topicID ?= data.routeQuery.topic_id
    if postID
        post = data.topicPosts?[topicID].find((post) -> post.id is postID)
    return div({className: 'spinner'}) if postID and not post

    fields = getFields(topicID, postID, data)

    if postID
        fields_ = mergeFieldsData(fields, {
            formData: {
                'post.replies_to_id': post.replies_to_id
                'post.kind': post.kind
                'post.body': post.body
            }
        })
    else
        fields_ = fields

    return div(
        {
            id: 'post-form'
            className: (if postID then 'update' else 'create') + ' col-6'
        }
        h1(if postID then 'Update Post' else 'Create Post')
        form(fields_)
    )
