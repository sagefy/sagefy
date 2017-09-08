const { required } = require('../../modules/validations')
const { extend } = require('../../modules/utilities')
const cardSchema = require('../card')

module.exports = extend({}, cardSchema, {
    'data.video_id': {
        type: 'text',
        validations: [required],
    },
    'data.site': {
        type: 'select',
        validations: [required],
        options: [{ value: 'youtube' }, { value: 'vimeo' }],
    },
})
