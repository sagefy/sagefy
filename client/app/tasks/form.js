const store = require('../modules/store')
const tasks = require('../modules/tasks')
const recorder = require('../modules/recorder')
const {validateFormData} = require('../modules/auxiliaries')

module.exports = tasks.add({
    updateFormData: (data) => {
        store.dispatch({
            data,
            message: 'update form data',
            type: 'SET_FORM_DATA',
        })
    },

    validateForm: (data, schema, fields) => {
        const errors = validateFormData(data, schema, fields)
        if (errors.length) {
            store.dispatch({
                type: 'SET_ERRORS',
                message: 'validate form - invalid',
                errors,
            })
            return errors
        }
        recorder.emit('validate form - valid')
    },

    addListFieldRow: (name, columns) => {
        store.dispatch({
            type: 'ADD_LIST_FIELD_ROW',
            message: 'add list field row',
            name,
            columns
        })
    },

    removeListFieldRow: (name, index) => {
        store.dispatch({
            type: 'REMOVE_LIST_FIELD_ROW',
            message: 'remove list field row',
            name,
            index
        })
    }
})
