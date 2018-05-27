const clone = require('lodash.clone')

module.exports = function topicPostVersions(
  state = {
    card: {},
    unit: {},
    subject: {},
  },
  action = { type: '' }
) {
  if (action.type === 'ADD_TOPIC_POST_VERSIONS_CARD') {
    state.card = clone(state.card)
    state.card[action.version.id] = action.version
    return state
  }
  if (action.type === 'ADD_TOPIC_POST_VERSIONS_UNIT') {
    state.unit = clone(state.unit)
    state.unit[action.version.id] = action.version
    return state
  }
  if (action.type === 'ADD_TOPIC_POST_VERSIONS_SUBJECT') {
    state.subject = clone(state.subject)
    state.subject[action.version.id] = action.version
    return state
  }
  return state
}
