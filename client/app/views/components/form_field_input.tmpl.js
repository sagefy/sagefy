const { input } = require('../../modules/tags')

module.exports = (data) => {
    return input({
        id: `ff-${data.name}`,
        name: data.name,
        placeholder: data.placeholder || '',
        type: data.type || 'text',
        value: data.value || data.default || '',
        size: data.size || 40,
    })
}
