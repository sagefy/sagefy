const { div, h1 } = require('../../modules/tags')
// const c = require('../../modules/content').get
const form = require('../components/form.tmpl')
const spinner = require('../components/spinner.tmpl')
const { extend } = require('../../modules/utilities')
const {
    createFieldsData,
    findGlobalErrors,
} = require('../../modules/auxiliaries')
const { getFields, getSchema } = require('./post_form.fn')

// TODO-1 Currently there is no way to update an existing entity from the UI,
//        you can only propose a new entity.

const classes = (formData) => {
    const postID = formData['post.id']
    const postKind = formData['post.kind']
    const entityKind = formData['post.entity_version.kind']
    const cardKind = formData['entity.kind']
    return [
        'page',
        postID ? 'update' : 'create',
        postKind ? `post-${postKind}` : '',
        entityKind ? `entity-${entityKind}` : '',
        cardKind ? `card-${cardKind}` : '',
    ].join(' ')
}

module.exports = (data) => {
    const [topicID, postID] = data.routeArgs
    let post
    if (postID) {
        post =
            data.topicPosts &&
            data.topicPosts[topicID].find(post => post.id === postID)
    }

    if (postID && !post) {
        return spinner()
    }

    const formData = extend({}, data.formData, {
        'post.id': postID,
        'post.topic_id': topicID,
        'post.replies_to_id':
            (post && post.replies_to_id) || data.routeQuery.replies_to_id,
        'post.kind': post && post.kind,
        'post.body': post && post.body,
        'post.response': post ? `${post.response}` : null,
        'post.name': post && post.name,
    })

    const fields = getFields(formData)
    fields.push({
        type: 'submit',
        name: 'submit',
        label: postID ? 'Update Post' : 'Create Post',
        icon: 'create',
    })

    const instanceFields = createFieldsData({
        schema: getSchema(formData),
        fields,
        errors: data.errors,
        formData,
        sending: data.sending,
    })

    const globalErrors = findGlobalErrors({
        fields: fields,
        errors: data.errors,
    })

    return div(
        {
            id: 'post-form',
            className: classes(formData),
        },
        h1(postID ? 'Update Post' : 'Create Post'),
        form({
            fields: instanceFields,
            errors: globalErrors,
        })
    )
}
