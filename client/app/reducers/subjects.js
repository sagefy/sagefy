const { shallowCopy } = require('../modules/utilities')

module.exports = function subjects(state = {}, action = { type: '' }) {
    if (action.type === 'ADD_SUBJECT') {
        state = shallowCopy(state)
        state[action.subject.entity_id] = action.subject
        return state
    }
    return state
}
