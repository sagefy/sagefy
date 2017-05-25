const {mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = function searchResults(state = [], action = {type: ''}) {
    if(action.type === 'RESET_SEARCH') {
        return []
    }
    if(action.type === 'ADD_SEARCH_RESULTS') {
        return mergeArraysByKey(
            state,
            action.results,
            'id'
        )
    }
    return state
}
