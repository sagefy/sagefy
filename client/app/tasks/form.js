const store = require('../modules/store')
const recorder = require('../modules/recorder')
const {validateFormData} = require('../modules/auxiliaries')

module.exports = store.add({
    updateFormData: (data) => {
        recorder.emit('update form data')
        store.data.formData = data
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
        // Let's find the highest index
        let maxIndex = -1
        Object.keys(store.data.formData).forEach(key => {
            if (key.indexOf(name) === 0) {
                key = key.replace(`${name}.`, '')
                const index = parseInt(key.match(/^\d+/))
                if (index > maxIndex) { maxIndex = index }
            }
        })
        const newIndex = maxIndex + 1
        columns.forEach(column => {
            store.data.formData[`${name}.${newIndex}.${column}`] = ''
        })
        store.change()
    },

    removeListFieldRow: (name, index) => {
        recorder.emit('remove list field row', name, index)

        const parseKey = (key) => {
            const matches = key.match(/^(.*)\.(\d+)\.(.*)$/)
            if (matches) {
                const [, pre, rowIndex, col] = matches
                return [pre, rowIndex, col]
            }
        }

        const getKeyIndex = (key) => {
            key = parseKey(key)
            if(key) { key = key[1] }
            return parseInt(key)
        }

        Object.keys(store.data.formData)
            .filter((key) => key.indexOf(name) === 0)
            .sort((keyA, keyB) => getKeyIndex(keyA) - getKeyIndex(keyB))
            .forEach((key) => {
                const rowIndex = getKeyIndex(key)
                if (rowIndex > index) {
                    const [pre, , col] = parseKey(key)
                    store.data.formData[`${pre}.${rowIndex - 1}.${col}`] =
                        store.data.formData[key]
                }
                if (rowIndex >= index) {
                    delete store.data.formData[key]
                }
            })
        store.change()
    }
})
