{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get
form = require('../components/form.tmpl')

getFields = (postID) ->
    fields = [{
        name: 'topic_id'
    }, {
        name: 'replies_to_id'
    }, {
        name: 'kind'
    }, {
        name: 'body'
    }]

    return fields

getPostID = (data) ->
    match = data.route.match(/^\/posts\/([\d\w]+)\/update$/)
    return match[1] if match
    return null

module.exports = (data) ->
    postID = getPostID(data)

    return div(
        {id: 'post-form', className: 'col-10'}
        h1(if postID then 'Update Post' else 'Create Post')
        form(getFields(postID))
    )
