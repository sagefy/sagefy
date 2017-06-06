module.exports = function cardFeedback(state = '', action = { type: '' }) {
    if(action.type === 'RESET_CARD_FEEDBACK') {
        return ''
    }
    if(action.type === 'SET_CARD_FEEDBACK') {
        return action.feedback
    }
    return state
}
