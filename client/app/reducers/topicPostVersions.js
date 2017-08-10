const { shallowCopy } = require('../modules/utilities')

module.exports = function topicPostVersions(
    state = {
        card: {},
        unit: {},
        subject: {},
    },
    action = { type: '' }
) {
    if (action.type === 'ADD_TOPIC_POST_VERSIONS_CARD') {
        state.card = shallowCopy(state.card)
        state.card[action.version.id] = action.version
        return state
    }
    if (action.type === 'ADD_TOPIC_POST_VERSIONS_UNIT') {
        state.unit = shallowCopy(state.unit)
        state.unit[action.version.id] = action.version
        return state
    }
    if (action.type === 'ADD_TOPIC_POST_VERSIONS_SUBJECT') {
        state.subject = shallowCopy(state.subject)
        state.subject[action.version.id] = action.version
        return state
    }
    return state
}
