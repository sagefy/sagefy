broker = require('../../modules/broker')
actions = require('../../modules/actions')

module.exports = broker.add({
    'submit #post-form.create form': (e, el) ->
        e.preventDefault() if e
        actions.createPost(getFormValues(el))

    'submit #post-form.update form': (e, el) ->
        e.preventDefault() if e
        actions.updatePost(getFormValues(el))
})
