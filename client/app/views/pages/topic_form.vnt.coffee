broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{closest} = require('../../modules/utilities')
{getFormValues, parseFormValues} = require('../../modules/auxiliaries')

module.exports = broker.add({
    'submit #topic-form.create form': (e, el) ->
        e.preventDefault() if e
        values = getFormValues(el)
        tasks.updateFormData(values)
        # errors = tasks.validateForm(values, schema, [...])
        # unless errors?.length, (...tab)
        values = parseFormValues(values)
        if values.post?.kind is 'proposal'
            values[values.post.entity_version.kind] = values.entity
            delete values.entity
        tasks.createTopic(values)

    'submit #topic-form.update form': (e, el) ->
        e.preventDefault() if e
        values = getFormValues(el)
        tasks.updateFormData(values)
        # errors = tasks.validateForm(values, schema, [...])
        # unless errors?.length, (...tab)
        values = parseFormValues(values)
        tasks.updateTopic(values)

    'change #topic-form.create [name="post.kind"]': (e, el) ->
        form = closest(el, document.body, 'form')
        values = getFormValues(form)
        tasks.updateFormData(values)

    'change #topic-form.create [name="post.entity_version.kind"]': (e, el) ->
        form = closest(el, document.body, 'form')
        values = getFormValues(form)
        tasks.updateFormData(values)

    'change #topic-form.create [name="entity.kind"]': (e, el) ->
        form = closest(el, document.body, 'form')
        values = getFormValues(form)
        tasks.updateFormData(values)
})
