const { required } = require('../../modules/validations')
const { extend } = require('../../modules/utilities')
const cardSchema = require('../card')

module.exports = extend({}, cardSchema, {
    video_id: {
        type: 'text',
        validations: [required]
    },
    site: {
        type: 'select',
        validations: [required],
        options: [
            { value: 'youtube' },
            { value: 'vimeo' }
        ]
    }
})
