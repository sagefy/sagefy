const {mergeArraysByKey} = require('../modules/auxiliaries')
const {shallowCopy} = require('../modules/utilities')

module.exports = function cardVersions(state = {}, action = {type: ''}) {
    if(action.type === 'ADD_CARD_VERSIONS') {
        let versions = state[action.id] || []
        versions = mergeArraysByKey(
            versions,
            action.versions,
            'entity_id'
        )
        state = shallowCopy(state)
        state[action.id] = versions
        return state
    }
    return state
}
