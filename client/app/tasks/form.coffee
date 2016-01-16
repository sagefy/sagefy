store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
{validateFormData} = require('../modules/auxiliaries')

module.exports = store.add({
    updateFormData: (data) ->
        recorder.emit('update form data')
        @data.formData = data
        @change()

    validateForm: (data, schema, fields) ->
        @data.errors = validateFormData(data, schema, fields)
        if @data.errors.length
            recorder.emit('validate form - invalid', @data.errors)
            @change()
            return @data.errors
        recorder.emit('validate form - valid')

    addListFieldRow: (name, columns) ->
        recorder.emit('add list field row', name, columns)

        # Let's find the highest index
        maxIndex = -1
        for key, value of @data.formData
            if key.indexOf(name) is 0
                key = key.replace("#{name}.", '')
                index = parseInt(key.match(/^\d+/))
                maxIndex = index if index > maxIndex

        newIndex = maxIndex + 1

        for column in columns
            @data.formData["#{name}.#{newIndex}.#{column}"] = ''

        @change()

    removeListFieldRow: (name, index) ->
        recorder.emit('remove list field row', name, index)

        parseKey = (key) ->
            matches = key.match(/^(.*)\.(\d+)\.(.*)$/)
            if matches
                [full, pre, rowIndex, col] = matches
                return [pre, rowIndex, col]

        getKeyIndex = (key) ->
            return parseInt(parseKey(key)?[1])

        Object.keys(@data.formData)
            .filter((key) -> key.indexOf(name) is 0)
            .sort((keyA, keyB) -> getKeyIndex(keyA) - getKeyIndex(keyB))
            .forEach((key) =>
                rowIndex = getKeyIndex(key)
                if rowIndex > index
                    [pre, _, col] = parseKey(key)
                    @data.formData["#{pre}.#{rowIndex - 1}.#{col}"] =
                        @data.formData[key]
                if rowIndex >= index
                    delete @data.formData[key]
            )
        @change()
})
