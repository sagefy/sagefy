broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{getFormValues} = require('../../modules/auxiliaries')

module.exports = broker.add({
    'submit #post-form.create form': (e, el) ->
        e.preventDefault() if e
        values = getFormValues(el)
        tasks.createPost(values)

    'submit #post-form.update form': (e, el) ->
        e.preventDefault() if e
        values = getFormValues(el)
        values.post.id = el.querySelector('button').id
        tasks.updatePost(values)
})
