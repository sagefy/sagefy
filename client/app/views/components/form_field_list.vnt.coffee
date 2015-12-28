broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{closest} = require('../../modules/utilities')

module.exports = broker.add({
    'click .form-field--list .remove-row': (e, el) ->
        e.preventDefault() if e
        row = closest(el, document.body, 'tr')
        # TODO@ now remove the row from the store

    'click .form-field--list .add-row': (e, el) ->
        e.preventDefault() if e
        # TODO@ add a new blank row to the store

    # TODO 'dragstart .form-field--list .move-row': (e, el) ->
    # TODO 'drop .form-field--list .move-row': (e, el) ->
})
