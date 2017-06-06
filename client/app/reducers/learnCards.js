const { shallowCopy } = require('../modules/utilities')

module.exports = function learnCards(state = {}, action = { type: '' }) {
    if (action.type === 'ADD_LEARN_CARD') {
        state = shallowCopy(state)
        state[action.id] = action.card
        return state
    }
    return state
}
