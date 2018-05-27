const get = require('lodash.get')
const merge = require('lodash.merge')
const { div, h1 } = require('../../helpers/tags')
// const c = require('../../helpers/content').get
const form = require('../components/form.tmpl')
const spinner = require('../components/spinner.tmpl')
const { createFieldsData, findGlobalErrors } = require('../../helpers/forms')
const { getFields, getSchema } = require('./post_form.fn')
const { getIsLoggedIn } = require('../../selectors/base')
const goLogin = require('../../helpers/go_login')

// TODO-1 Currently there is no way to update an existing entity from the UI,
//    you can only propose a new entity.

const classes = formData => {
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

module.exports = data => {
  if (getIsLoggedIn(data) === null) {
    return spinner()
  }

  if (!getIsLoggedIn(data)) {
    return goLogin()
  }

  const [topicID, postID] = data.routeArgs
  const post = get(data, `topicPosts[${topicID}]`, []).find(
    xpost => xpost.id === postID
  )

  if (postID && !post) {
    return spinner()
  }

  const formData = merge({}, data.formData, {
    'post.id': postID,
    'post.topic_id': topicID,
    'post.replies_to_id': get(
      post,
      'replies_to_id',
      data.routeQuery.replies_to_id
    ),
    'post.kind': get(post, 'kind'),
    'post.body': get(post, 'body'),
    'post.response': post ? `${post.response}` : null,
    'post.name': get(post, 'name'),
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
    fields,
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
