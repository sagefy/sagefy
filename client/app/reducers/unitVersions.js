const mergeArraysByKey = require('../helpers/merge_arrays_by_key')
const clone = require('lodash.clone')

module.exports = function unitVersions(state = {}, action = { type: '' }) {
  if (action.type === 'ADD_UNIT_VERSIONS') {
    let versions = state[action.entity_id] || []
    versions = mergeArraysByKey(
      versions,
      action.versions,
      'id' // id is the version id
    )
    state = clone(state)
    state[action.entity_id] = versions
    return state
  }
  return state
}
