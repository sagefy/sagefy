{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get
form = require('../components/form.tmpl')
{extend} = require('../../modules/utilities')
{createFieldsData} = require('../../modules/auxiliaries')
{getFields, getSchema} = require('./post_form.fn')

# TODO-1 Currently there is no way to update an existing entity from the UI,
#        you can only propose a new entity.

classes = (formData) ->
    postID = formData['post.id']
    postKind = formData['post.kind']
    entityKind = formData['post.entity_version.kind']
    cardKind = formData['entity.kind']
    return [
        if postID then 'update' else 'create'
        if postKind then "post-#{postKind}" else ''
        if entityKind then "entity-#{entityKind}" else ''
        if cardKind then "card-#{cardKind}" else ''
    ].join(' ')

module.exports = (data) ->
    [topicID, postID] = data.routeArgs
    if postID
        post = data.topicPosts?[topicID].find((post) -> post.id is postID)

    return spinner() if postID and not post

    formData = extend({}, data.formData, {
        'post.id': postID
        'post.topic_id': topicID
        'post.replies_to_id': post?.replies_to_id \
                              or data.routeQuery.replies_to_id
        'post.kind': post?.kind
        'post.body': post?.body
        'post.response': if post then '' + post.response
        'post.name': post?.name
    })

    fields = getFields(formData)
    fields.push({
        type: 'submit'
        name: 'submit'
        label: if postID then 'Update Post' else 'Create Post'
        icon: 'create'
    })

    instanceFields = createFieldsData({
        schema: getSchema(formData)
        fields: fields
        errors: data.errors
        formData: formData
        sending: data.sending
    })

    return div(
        {
            id: 'post-form'
            className: classes(formData)
        }
        h1(if postID then 'Update Post' else 'Create Post')
        form(instanceFields)
    )
