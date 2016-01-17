{textarea} = require('../../modules/tags')

module.exports = (data) ->
    return textarea({
        id: "ff-#{data.name}"
        name: data.name
        placeholder: data.placeholder or ''
        cols: data.cols or 40
        rows: data.rows or 4
    }, data.value or '')
