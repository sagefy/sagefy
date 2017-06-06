
module.exports = function formData(state = {}, action = { type: '' }) {
    if (action.type === 'RESET_FORM_DATA') {
        return {}
    }
    if (action.type === 'SET_FORM_DATA') {
        return action.data
    }
    return state
}
