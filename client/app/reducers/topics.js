const { shallowCopy } = require('../modules/utilities')

module.exports = function topics(state = {}, action = { type: '' }) {
    if (action.type === 'ADD_TOPIC') {
        state = shallowCopy(state)
        state[action.id || action.topic.id] = action.topic
        return state
    }
    return state
}
