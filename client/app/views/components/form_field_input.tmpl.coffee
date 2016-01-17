{input} = require('../../modules/tags')

module.exports = (data) ->
    return input({
        id: "ff-#{data.name}"
        name: data.name
        placeholder: data.placeholder or ''
        type: data.type or 'text'
        value: data.value or data.default or ''
        size: data.size or 40
    })
