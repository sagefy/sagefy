const { mergeArraysByKey } = require('../helpers/auxiliaries')
const { shallowCopy } = require('../helpers/utilities')

module.exports = function unitVersions(state = {}, action = { type: '' }) {
  if (action.type === 'ADD_UNIT_VERSIONS') {
    let versions = state[action.entity_id] || []
    versions = mergeArraysByKey(
      versions,
      action.versions,
      'id' // id is the version id
    )
    state = shallowCopy(state)
    state[action.entity_id] = versions
    return state
  }
  return state
}
