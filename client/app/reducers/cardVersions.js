const { mergeArraysByKey } = require('../modules/auxiliaries')
const { shallowCopy } = require('../modules/utilities')

module.exports = function cardVersions(state = {}, action = { type: '' }) {
    if (action.type === 'ADD_CARD_VERSIONS') {
        let versions = state[action.entity_id] || []
        versions = mergeArraysByKey(
            versions,
            action.versions,
            'id' // id is the version id
        )
        state = shallowCopy(state)
        state[action.entity_id] = versions
        return state
    }
    return state
}
