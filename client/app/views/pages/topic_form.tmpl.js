const get = require('lodash.get')
const merge = require('lodash.merge')
const capitalize = require('lodash.capitalize')
const { div, h1, p, strong } = require('../../helpers/tags')
const form = require('../components/form.tmpl')
const getPostFields = require('./post_form.fn').getFields
const getPostSchema = require('./post_form.fn').getSchema
const {
  createFieldsData,
  prefixObjectKeys,
  findGlobalErrors,
} = require('../../helpers/forms')
const topicSchema = require('../../schemas/topic')
const spinner = require('../components/spinner.tmpl')
const { getIsLoggedIn } = require('../../selectors/base')
const goLogin = require('../../helpers/go_login')

const classes = formData => {
  const topicID = formData['topic.id']
  const postKind = formData['post.kind']
  const entityKind = formData['post.entity_version.kind']
  const cardKind = formData['entity.kind']
  return [
    'page',
    topicID ? 'update' : 'create',
    postKind ? `post-${postKind}` : '',
    entityKind ? `entity-${entityKind}` : '',
    cardKind ? `card-${cardKind}` : '',
  ].join(' ')
}

const getFields = formData => {
  let fields = []
  if (formData['topic.id']) {
    fields.push({
      name: 'topic.id',
    })
  }
  fields = fields.concat([
    {
      name: 'topic.entity_id',
    },
    {
      name: 'topic.entity_kind',
    },
    {
      name: 'topic.name',
      label: 'Topic Name',
    },
  ])
  return fields
}

const getTopicID = data => {
  const match = data.route.match(/^\/topics\/([\d\w\-_]+)\/update$/)
  if (match) {
    return match[1]
  }
  return null
}

const getEntityByKind = (data, kind, id) => {
  if (kind === 'card') {
    return data.cards && data.cards[id]
  }
  if (kind === 'unit') {
    return data.units && data.units[id]
  }
  if (kind === 'subject') {
    return data.subjects && data.subjects[id]
  }
  return null
}

const getEntitySummary = data => {
  const topicID = getTopicID(data)
  let topic
  let { kind } = data.routeQuery
  let { id } = data.routeQuery

  if (topicID) {
    topic = data.topics && data.topics[topicID]
    kind = topic.entity_kind
    id = topic.entity_id
  }

  const entity = getEntityByKind(data, kind, id)

  return {
    name: get(entity, 'name'),
    kind,
  }
}

module.exports = data => {
  if (getIsLoggedIn(data) === null) {
    return spinner()
  }

  if (!getIsLoggedIn(data)) {
    return goLogin()
  }

  const topicID = getTopicID(data)
  const topic = get(data, `topics[${topicID}]`, null)

  if (topicID && !topic) {
    return spinner()
  }

  const formData = merge({}, data.formData, {
    'topic.id': get(topic, 'id'),
    'topic.name': get(topic, 'name'),
    'topic.entity_kind': get(topic, 'entity_kind', data.routeQuery.kind),
    'topic.entity_id': get(topic, 'entity_id', data.routeQuery.id),
  })

  let fields = getFields(formData)

  const schema = prefixObjectKeys('topic.', topicSchema)

  if (!formData['topic.id']) {
    fields = fields.concat(getPostFields(formData))
    merge(schema, getPostSchema(formData))
  }
  fields.push({
    type: 'submit',
    name: 'submit',
    label: topicID ? 'Update Topic' : 'Create Topic',
    icon: 'create',
  })

  const instanceFields = createFieldsData({
    schema,
    fields,
    errors: data.errors,
    formData,
    sending: data.sending,
  })

  const globalErrors = findGlobalErrors({
    fields,
    errors: data.errors,
  })

  const entity = getEntitySummary(data)

  return div(
    {
      id: 'topic-form',
      className: classes(formData),
    },
    h1(topicID ? 'Update Topic' : 'Create Topic'),
    p(
      strong(capitalize(get(entity, 'kind', ''))),
      `: ${get(entity, 'name', '')}`
    ),
    form({
      fields: instanceFields,
      errors: globalErrors,
    })
  )
}
