const { shallowCopy } = require('../modules/utilities')

module.exports = function units(state = {}, action = { type: '' }) {
    if (action.type === 'ADD_UNIT') {
        state = shallowCopy(state)
        state[action.unit.entity_id] = action.unit
        return state
    }
    return state
}
