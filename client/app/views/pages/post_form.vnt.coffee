broker = require('../../modules/broker')
actions = require('../../modules/actions')
{getFormValues} = require('../../modules/auxiliaries')

module.exports = broker.add({
    'submit #post-form.create form': (e, el) ->
        e.preventDefault() if e
        values = getFormValues(el)
        actions.createPost(values)

    'submit #post-form.update form': (e, el) ->
        e.preventDefault() if e
        actions.updatePost(getFormValues(el))
})
