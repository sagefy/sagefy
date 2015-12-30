broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{getFormValues} = require('../../modules/auxiliaries')

module.exports = broker.add({
    'submit #topic-form.create form': (e, el) ->
        e.preventDefault() if e

        if values.post.kind is 'proposal'
            values[values.entity_kind] = values.entity
            delete values.entity
            delete values.entity_kind

        tasks.createTopic(values)

    'submit #topic-form.update form': (e, el) ->
        e.preventDefault() if e
        values = getFormValues(el)
        values.topic.id = el.querySelector('button').id
        tasks.updateTopic(values)

    'change #topic-form.create [name="post.kind"]': (e, el) ->
        tasks.changePostKind(el.value)

    'change #topic-form.create [name="entity_kind"]': (e, el) ->
        tasks.changeEntityKind(el.value)

    'change #topic-form.create [name="entity.kind"]': (e, el) ->
        tasks.changeCardKind(el.value)
})
