module.exports = function passwordPageState(state = '', action = { type: '' }) {
    if(action.type === 'SET_PASSWORD_PAGE_STATE') {
        return action.state
    }
    return state
}
