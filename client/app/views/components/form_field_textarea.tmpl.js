const { textarea } = require('../../modules/tags')

module.exports = data =>
    textarea(
        {
            id: `ff-${data.name}`,
            name: data.name,
            placeholder: data.placeholder || '',
            cols: data.cols || 40,
            rows: data.rows || 4,
        },
        data.value || ''
    )
