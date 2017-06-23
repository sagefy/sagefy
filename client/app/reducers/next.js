module.exports = function next(state = {}, action = { type: '' }) {
    if (action.type === 'SET_NEXT') {
        return action.next
    }
    return state
}
