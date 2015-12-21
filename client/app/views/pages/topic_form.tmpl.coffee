{div, h1, p, strong} = require('../../modules/tags')
c = require('../../modules/content').get
form = require('../components/form.tmpl')
postSchema = require('../../schemas/post')
topicSchema = require('../../schemas/topic')
{extend} = require('../../modules/utilities')
{mergeFieldsData, ucfirst} = require('../../modules/auxiliaries')
getPostFields = require('./post_form.fn').getFields

getFields = ({topicID, entityID, entityKind, postKind = 'post'}) ->
    fields = [extend({
        name: 'topic.entity.id'
        value: entityID
    }, topicSchema['entity.id']), extend({
        name: 'topic.entity.kind'
        value: entityKind
    }, topicSchema['entity.kind']), extend({
        name: 'topic.name'
        label: 'Topic Name'
    }, topicSchema.name)]

    unless topicID
        fields = fields.concat(getPostFields({
            editKind: true
            postKind
        }))

    fields.push({
        id: topicID
        type: 'submit'
        name: 'submit'
        label: if topicID then 'Update Topic' else 'Create Topic'
        icon: 'plus'
    })

    return fields

getTopicID = (data) ->
    match = data.route.match(/^\/topics\/([\d\w]+)\/update$/)
    return match[1] if match
    return null

getEntity = (data, kind, id) ->
    if kind is 'card'
        return data.cards?[id]

    if kind is 'unit'
        return data.units?[id]

    if kind is 'set'
        return data.sets?[id]


spinner = ->
    return div({className: 'spinner'})

module.exports = (data) ->
    topicID = getTopicID(data)

    if topicID
        topic = data.topics?[topicID]
        return spinner() if not topic
        entityKind = topic.entity.kind
        entityID = topic.entity.id
        entity = getEntity(data, entityKind, entityID)
        entityName = entity?.name
    else
        entityKind = data.routeQuery.kind
        entityID = data.routeQuery.id
        entity = getEntity(data, entityKind, entityID)
        entityName = entity?.name

    fields = getFields({
        topicID
        entityID
        entityKind
        postKind: data.postKind
    })

    fields_ = if topicID
        mergeFieldsData(fields, {formData: {
            'topic.name': topic.name
        }})
    else
        fields

    return div(
        {
            id: 'topic-form'
            className: (if topicID then 'update' else 'create') + ' col-8'
        }
        h1(if topicID then 'Update Topic' else 'Create Topic')
        p(
            {className: 'leading'}
            strong(ucfirst(entityKind))
            ": #{entityName}"
        )
        form(fields_)
    )
