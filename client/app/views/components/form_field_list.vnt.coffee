broker = require('../../modules/broker')
tasks = require('../../modules/tasks')
{closest} = require('../../modules/utilities')
{getFormValues} = require('../../modules/auxiliaries')

module.exports = broker.add({
    'click .form-field--list .remove-row': (e, el) ->
        e.preventDefault() if e

        form = closest(el, 'form')
        values = getFormValues(form)
        tasks.updateFormData(values)

        table = closest(el, 'table')
        name = table.dataset.name
        index = parseInt(el.dataset.index)
        tasks.removeListFieldRow(name, index)

    'click .form-field--list .add-row': (e, el) ->
        e.preventDefault() if e

        form = closest(el, 'form')
        values = getFormValues(form)
        tasks.updateFormData(values)

        table = closest(el, 'table')
        name = table.dataset.name
        columns = Array.prototype.map.call(
            table.querySelectorAll('th')
            (el) -> el.dataset.col
        ).filter((c) -> c)
        tasks.addListFieldRow(name, columns)

    # TODO-3 'dragstart .form-field--list .move-row': (e, el) ->
    # TODO-3 'drop .form-field--list .move-row': (e, el) ->
})
