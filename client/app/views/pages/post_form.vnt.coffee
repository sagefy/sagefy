broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{closest} = require('../../modules/utilities')
{getFormValues, parseFormValues} = require('../../modules/auxiliaries')

module.exports = broker.add({
    'submit #post-form.create form': (e, el) ->
        e.preventDefault() if e
        values = getFormValues(el)
        tasks.updateFormData(values)
        # errors = tasks.validateForm(values, schema, [...])
        # unless errors?.length, (...tab)
        values = parseFormValues(values)
        if values.post?.kind is 'proposal'
            if values.entity?.require_ids
                values.entity.require_ids = values.entity.require_ids
                    .map((r) -> r.id)
            if values.post?.entity_version?.kind
                values[values.post.entity_version.kind] = values.entity
                delete values.entity
        tasks.createPost(values)

    'submit #post-form.update form': (e, el) ->
        e.preventDefault() if e
        values = getFormValues(el)
        tasks.updateFormData(values)
        # errors = tasks.validateForm(values, schema, [...])
        # unless errors?.length, (...tab)
        values = parseFormValues(values)
        tasks.updatePost(values)

    'change #post-form.create [name="post.kind"]': (e, el) ->
        form = closest(el, document.body, 'form')
        values = getFormValues(form)
        tasks.updateFormData(values)

    'change #post-form.create [name="post.entity_version.kind"]': (e, el) ->
        form = closest(el, document.body, 'form')
        values = getFormValues(form)
        tasks.updateFormData(values)

    'change #post-form.create [name="entity.kind"]': (e, el) ->
        form = closest(el, document.body, 'form')
        values = getFormValues(form)
        tasks.updateFormData(values)
})
