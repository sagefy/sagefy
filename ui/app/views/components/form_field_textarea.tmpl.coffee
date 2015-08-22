module.exports = (data) ->
    return textarea({
        id: data.name
        name: data.name
        placeholder: data.placeholder or ''
        cols: data.cols or ''
        rows: data.rows or ''
    }, data.value or '')
