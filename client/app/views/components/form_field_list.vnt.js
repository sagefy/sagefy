const broker = require('../../modules/broker')
const tasks = require('../../modules/tasks')
const { closest } = require('../../modules/utilities')
const { getFormValues } = require('../../modules/auxiliaries')

module.exports = broker.add({
    'click .form-field--list__remove-row'(e, el) {
        if (e) { e.preventDefault() }
        const form = closest(el, 'form')
        const values = getFormValues(form)
        const table = closest(el, 'table')
        const name = table.dataset.name
        const index = parseInt(el.dataset.index)
        tasks.removeListFieldRow(values, name, index)
    },

    'click .form-field--list__add-row'(e, el) {
        if (e) { e.preventDefault() }
        const form = closest(el, 'form')
        const values = getFormValues(form)
        const table = closest(el, 'table')
        const name = table.dataset.name
        const columns = Array.prototype.map.call(
            table.querySelectorAll('th'),
            el => el.dataset.col
        ).filter(c => c)
        tasks.addListFieldRow(values, name, columns)
    },

    // TODO-3 'dragstart .form-field--list__move-row'(e, el)
    // TODO-3 'drop form-field--list__move-row'(e, el)
})
