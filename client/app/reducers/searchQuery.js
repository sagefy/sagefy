module.exports = function searchQuery(state = '', action = {type: ''}) {
    if(action.type === 'RESET_SEARCH_RESULTS') {
        return ''
    }
    if(action.type === 'SET_SEARCH_QUERY') {
        return action.q
    }
    return state
}
