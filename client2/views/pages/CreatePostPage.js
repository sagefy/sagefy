/*

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



// TODO-2 add `available` field
// TODO-2 on update: how to decline a proposal?
// TODO-3 Tags (all)

const merge = require('lodash.merge')
const { prefixObjectKeys } = require('../../helpers/forms')

const postSchema = require('../../schemas/post')
const voteSchema = require('../../schemas/vote')
const proposalSchema = require('../../schemas/proposal')

const schemas = {
  post: postSchema,
  vote: voteSchema,
  proposal: proposalSchema,
}

const getFields = formData => {
  const fields = []
  ;['post.id', 'post.topic_id', 'post.replies_to_id'].forEach(name => {
    if (formData[name]) {
      fields.push({ name })
    }
  })

  /* PP@ fields.push({
    name: 'post.kind',
    options: [{
      label: 'Post',
      disabled: !!formData['post.id'],
    }, {
      label: 'Proposal',
      disabled: !!formData['post.id'],
    }, {
      label: 'Vote',
      disabled: !!formData['post.id'] ||
            !formData['post.replies_to_id']
    }],
    inline: true,
    label: 'Post Kind'
  }) /

  fields.push({
    name: 'post.kind',
    type: 'hidden',
  })

  if (formData['post.kind'] === 'vote') {
    fields.push({
      name: 'post.response',
      options: [{ label: 'Yes, I agree' }, { label: 'No, I dissent' }],
      inline: true,
      label: 'Response',
      disabled: !!formData['post.id'],
    })
  }

  fields.push({
    name: 'post.body',
    label:
      formData['post.kind'] === 'proposal' ? 'Proposal Summary' : 'Post Body',
    description:
      formData['post.kind'] === 'proposal'
        ? 'Describe the value of this proposal.'
        : null,
  })

  // TODO PP@ update proposal handling

  return fields
}

const getSchema = formData => {
  const schema = {}

  if (formData['post.kind'] === 'proposal') {
    merge(schema, prefixObjectKeys('post.', schemas.proposal))
  } else if (formData['post.kind'] === 'vote') {
    merge(schema, prefixObjectKeys('post.', schemas.vote))
  } else {
    merge(schema, prefixObjectKeys('post.', schemas.post))
  }

  return schema
}

module.exports = { getFields, getSchema }






const { getFormValues, parseFormValues } = require('../../helpers/forms')

module.exports = (store, broker) => {
  const { getTasks } = store
  broker.add({
    'submit #post-form.create form'(e, el) {
      if (e) {
        e.preventDefault()
      }
      let values = getFormValues(el)
      getTasks().updateFormData(values)
      // errors = tasks.validateForm(values, schema, [...])
      // unless errors?.length, (...tab)
      values = parseFormValues(values)
      /* PP@ if (values.post && values.post.kind === 'proposal') {
      if (values.entity && values.entity.require_ids) {
        values.entity.require_ids = values.entity.require_ids
          .map((require) => require.id).filter((require) => require)
      }
      if (values.post &&
        values.post.entity_version
        && values.post.entity_version.kind) {
        values[values.post.entity_version.kind] = values.entity
        delete values.entity
      }
    } /
      getTasks().createPost(values)
    },

    'submit #post-form.update form'(e, el) {
      if (e) {
        e.preventDefault()
      }
      let values = getFormValues(el)
      getTasks().updateFormData(values)
      // errors = tasks.validateForm(values, schema, [...])
      // unless errors?.length, (...tab)
      values = parseFormValues(values)
      getTasks().updatePost(values)
    },
  })
}


*/
