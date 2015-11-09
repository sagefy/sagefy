{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get
form = require('../components/form.tmpl')
postSchema = require('../../schemas/post')
{extend} = require('../../modules/utilities')

getFields = (postID) ->
    fields = [extend({
        name: 'post.topic_id'
    }, postSchema.topic_id), extend({
        name: 'post.replies_to_id'
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
        type: 'submit'
        name: 'submit'
        label: if postID then 'Update Post' else 'Create Post'
        icon: 'plus'
    }]

    return fields

getPostID = (data) ->
    match = data.route.match(/^\/posts\/([\d\w]+)\/update$/)
    return match[1] if match
    return null

module.exports = (data) ->
    postID = getPostID(data)
    # TODO return div({className: 'spinner'}) unless ...

    return div(
        {
            id: 'post-form'
            className: (if postID then 'update' else 'create') + ' col-6'
        }
        h1(if postID then 'Update Post' else 'Create Post')
        form(getFields(postID))
    )
