const mergeArraysByKey = require('../helpers/merge_arrays_by_key')

module.exports = function searchResults(state = [], action = { type: '' }) {
  if (action.type === 'RESET_SEARCH') {
    return []
  }
  if (action.type === 'ADD_SEARCH_RESULTS') {
    return mergeArraysByKey(state, action.results, 'id')
  }
  return state
}
