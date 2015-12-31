store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
{validateFormData} = require('../modules/auxiliaries')

module.exports = store.add({
    updateFormData: (data) ->
        @data.formData = data
        @change()

    validateForm: (data, schema, fields) ->
        @data.errors = validateFormData(data, schema, fields)
        if @data.errors.length
            recorder.emit('invalid form', @data.errors)
            @change()
            return @data.errors
})
