const {div, h1, p, strong} = require('../../modules/tags')
const form = require('../components/form.tmpl')
const getPostFields = require('./post_form.fn').getFields
const getPostSchema = require('./post_form.fn').getSchema
const {createFieldsData, prefixObjectKeys, ucfirst} =
    require('../../modules/auxiliaries')
const {extend} = require('../../modules/utilities')
const topicSchema = require('../../schemas/topic')
const spinner = require('../components/spinner.tmpl')

const classes = (formData) => {
    const topicID = formData['topic.id']
    const postKind = formData['post.kind']
    const entityKind = formData['post.entity_version.kind']
    const cardKind = formData['entity.kind']
    return [
        topicID ? 'update' : 'create',
        postKind ? `post-${postKind}` : '',
        entityKind ? `entity-${entityKind}` : '',
        cardKind ? `card-${cardKind}` : ''
    ].join(' ')
}

const getFields = (formData) => {
    let fields = []
    if (formData['topic.id']) {
        fields.push({
            name: 'topic.id'
        })
    }
    fields = fields.concat([{
        name: 'topic.entity.id'
    }, {
        name: 'topic.entity.kind'
    }, {
        name: 'topic.name',
        label: 'Topic Name'
    }])
    return fields
}

const getTopicID = (data) => {
    const match = data.route.match(/^\/topics\/([\d\w]+)\/update$/)
    if(match) { return match[1] }
    return null
}

const getEntityByKind = (data, kind, id) => {
    if (kind === 'card') {
        return data.cards && data.cards[id]
    }
    if (kind === 'unit') {
        return data.units && data.units[id]
    }
    if (kind === 'set') {
        return data.sets && data.sets[id]
    }
}

const getEntitySummary = (data) => {
    const topicID = getTopicID(data)
    let topic, kind, id

    if (topicID) {
        topic = data.topics && data.topics[topicID]
        kind = topic.entity.kind
        id = topic.entity.id
    } else {
        kind = data.routeQuery.kind
        id = data.routeQuery.id
    }

    const entity = getEntityByKind(data, kind, id)

    return {
        name: entity && entity.name,
        kind: kind
    }
}

module.exports = (data) => {
    const topicID = getTopicID(data)
    let topic
    if (topicID) {
        topic = data.topics && data.topics[topicID]
    }

    if(topicID && !topic) { return spinner() }

    const formData = extend({}, data.formData, {
        'topic.id': topic && topic.id,
        'topic.name': topic && topic.name,
        'topic.entity.kind': topic && topic.entity.kind || data.routeQuery.kind,
        'topic.entity.id': topic && topic.entity.kind || data.routeQuery.id
    })

    let fields = getFields(formData)

    const schema = prefixObjectKeys('topic.', topicSchema)

    if (! formData['topic.id']) {
        fields = fields.concat(getPostFields(formData))
        extend(schema, getPostSchema(formData))
    }
    fields.push({
        type: 'submit',
        name: 'submit',
        label: topicID ? 'Update Topic' : 'Create Topic',
        icon: 'create'
    })

    const instanceFields = createFieldsData({
        schema: schema,
        fields: fields,
        errors: data.errors,
        formData: formData,
        sending: data.sending,
    })

    const entity = getEntitySummary(data)

    return div(
        {
            id: 'topic-form',
            className: classes(formData)
        },
        h1(topicID ? 'Update Topic' : 'Create Topic'),
        p(
            strong(ucfirst((entity && entity.kind) || '')),
            `: ${entity && entity.name}`
        ),
        form(instanceFields)
    )
}
