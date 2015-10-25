broker = require('../../modules/broker')
actions = require('../../modules/actions')
{getFormValues} = require('../../modules/auxiliaries')

module.exports = broker.add({
    'submit #topic-form.create form': (e, el) ->
        e.preventDefault() if e
        actions.createTopic(getFormValues(el))

    'submit #topic-form.update form': (e, el) ->
        e.preventDefault() if e
        actions.updateTopic(getFormValues(el))
})
