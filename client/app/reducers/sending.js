module.exports = function sending(state = false, action = {type: ''}) {
    if(action.type === 'SET_SENDING_ON') {
        return true
    }
    if(action.type === 'SET_SENDING_OFF') {
        return false
    }
    return state
}
