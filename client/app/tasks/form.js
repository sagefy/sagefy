const store = require('../modules/store')
const tasks = require('../modules/tasks')
const recorder = require('../modules/recorder')
const {validateFormData} = require('../modules/auxiliaries')
const formData = require('../reducers/formData')
const errorsReducer = require('../reducers/errors')

module.exports = tasks.add({
    updateFormData: (data) => {
        store.update('formData', formData, {
            data,
            message: 'update form data',
            type: 'SET_FORM_DATA',
        })
    },

    validateForm: (data, schema, fields) => {
        const errors = validateFormData(data, schema, fields)
        if (errors.length) {
            store.update('errors', errorsReducer, {
                type: 'SET_ERRORS',
                message: 'validate form - invalid',
                errors,
            })
            return errors
        }
        recorder.emit('validate form - valid')
    },

    addListFieldRow: (name, columns) => {
        store.update('formData', formData, {
            type: 'ADD_LIST_FIELD_ROW',
            message: 'add list field row',
            name,
            columns
        })
    },

    removeListFieldRow: (name, index) => {
        store.update('formData', formData, {
            type: 'REMOVE_LIST_FIELD_ROW',
            message: 'remove list field row',
            name,
            index
        })
    }
})
