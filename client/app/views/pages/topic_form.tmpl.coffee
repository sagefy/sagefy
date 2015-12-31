{div, h1, p, strong} = require('../../modules/tags')
form = require('../components/form.tmpl')
getPostFields = require('./post_form.fn').getFields
getPostSchema = require('./post_form.fn').getSchema
{createFieldsData, prefixObjectKeys, ucfirst} =
    require('../../modules/auxiliaries')
{extend} = require('../../modules/utilities')
topicSchema = require('../../schemas/topic')

classes = (formData) ->
    postID = formData['post.id']
    postKind = formData['post.kind']
    entityKind = formData['entity_kind']
    cardKind = formData['entity.kind']
    return [
        'col-6'
        if postID then 'update' else 'create'
        if postKind then "post-#{postKind}" else ''
        if entityKind then "entity-#{entityKind}" else ''
        if cardKind then "card-#{cardKind}" else ''
    ].join(' ')

getFields = (formData) ->
    fields = []

    if formData['topic.id']
        fields.push({
            name: 'topic.id'
        })

    fields = fields.concat([{
        name: 'topic.entity.id'
    }, {
        name: 'topic.entity.kind'
    }, {
        name: 'topic.name'
        label: 'Topic Name'
    }])
    
    return fields

getTopicID = (data) ->
    match = data.route.match(/^\/topics\/([\d\w]+)\/update$/)
    return match[1] if match
    return null

getEntityByKind = (data, kind, id) ->
    if kind is 'card'
        return data.cards?[id]

    if kind is 'unit'
        return data.units?[id]

    if kind is 'set'
        return data.sets?[id]

getEntitySummary = (data) ->
    topicID = getTopicID(data)

    if topicID
        topic = data.topics?[topicID]
        kind = topic.entity.kind
        id = topic.entity.id
    else
        kind = data.routeQuery.kind
        id = data.routeQuery.id

    entity = getEntityByKind(data, kind, id)

    return {
        name: entity?.name
        kind: kind
    }

module.exports = (data) ->
    topicID = getTopicID(data)
    if topicID
        topic = data.topics?[topicID]
    return div({className: 'spinner'}) if topicID and not topic

    formData = extend({}, data.formData, {
        'topic.id': topic?.id
        'topic.name': topic?.name
        'topic.entity.kind': topic?.entity.kind or data.routeQuery.kind
        'topic.entity.id': topic?.entity.kind or data.routeQuery.id
    })

    fields = getFields(formData)

    schema = prefixObjectKeys('topic.', topicSchema)

    if not formData['topic.id']
        fields = fields.concat(getPostFields(formData))
        extend(schema, getPostSchema(formData))

    fields.push({
        type: 'submit'
        name: 'submit'
        label: if topicID then 'Update Topic' else 'Create Topic'
        icon: 'plus'
    })

    instanceFields = createFieldsData({
        schema: schema
        fields: fields
        errors: data.errors
        formData: formData
        sending: data.sending
    })

    entity = getEntitySummary(data)

    return div(
        {
            id: 'topic-form'
            className: classes(formData)
        }
        h1(if topicID then 'Update Topic' else 'Create Topic')
        p(
            {className: 'leading'}
            strong(ucfirst(entity?.kind or ''))
            ": #{entity?.name}"
        )
        form(instanceFields)
    )
