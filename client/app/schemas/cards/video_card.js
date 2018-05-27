const { required } = require('../../helpers/validations')
const { extend } = require('../../helpers/utilities')
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
