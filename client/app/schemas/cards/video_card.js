const merge = require('lodash.merge')
const { required } = require('../../helpers/validations')
const cardSchema = require('../card')

module.exports = merge({}, cardSchema, {
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
