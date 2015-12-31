broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{closest} = require('../../modules/utilities')

module.exports = broker.add({
    'click .form-field--list .remove-row': (e, el) ->
        e.preventDefault() if e
        row = closest(el, document.body, 'tr')
        # TODO-0 now remove the row from the store

    'click .form-field--list .add-row': (e, el) ->
        e.preventDefault() if e
        # TODO-0 add a new blank row to the store

    # TODO-3 'dragstart .form-field--list .move-row': (e, el) ->
    # TODO-3 'drop .form-field--list .move-row': (e, el) ->
})
