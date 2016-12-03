module.exports = function cardResponse(state = {}, action = {type: ''}) {
    if(action.type === 'RESET_CARD_RESPONSE') {
        return {}
    }
    if(action.type === 'SET_CARD_RESPONSE') {
        return action.response
    }
    return state
}
