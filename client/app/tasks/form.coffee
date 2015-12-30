store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')

module.exports = store.add({
    updateFormData: (data) ->
        @data.formData = data
        @change()
})
