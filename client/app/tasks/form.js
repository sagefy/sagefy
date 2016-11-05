const store = require('../modules/store')
const recorder = require('../modules/recorder')
const {validateFormData} = require('../modules/auxiliaries')
const formData = require('../reducers/formData')

module.exports = store.add({
    updateFormData: (data) => {
        recorder.emit('update form data')
        store.update('formData', formData, {
            data,
            type: 'SET_FORM_DATA'
        })
        store.change()
    },

    validateForm: (data, schema, fields) => {
        store.data.errors = validateFormData(data, schema, fields)
        if (store.data.errors.length) {
            recorder.emit('validate form - invalid', store.data.errors)
            store.change()
            return store.data.errors
        }
        recorder.emit('validate form - valid')
    },

    addListFieldRow: (name, columns) => {
        recorder.emit('add list field row', name, columns)
        store.update('formData', formData, {
            type: 'ADD_LIST_FIELD_ROW',
            name,
            columns
        })
        store.change()
    },

    removeListFieldRow: (name, index) => {
        recorder.emit('remove list field row', name, index)
        store.update('formData', formData, {
            type: 'REMOVE_LIST_FIELD_ROW',
            name,
            index
        })
        store.change()
    }
})
