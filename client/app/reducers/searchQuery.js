module.exports = function searchQuery(state = '', action = { type: '' }) {
    if(action.type === 'RESET_SEARCH') {
        return ''
    }
    if(action.type === 'SET_SEARCH_QUERY') {
        return action.q
    }
    return state
}
