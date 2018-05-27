const { mergeArraysByKey } = require('../helpers/auxiliaries')

module.exports = function followsReducer(state = [], action = { type: '' }) {
  if (action.type === 'LIST_FOLLOWS_SUCCESS') {
    return mergeArraysByKey(state, action.follows, 'id')
  }
  if (action.type === 'ASK_FOLLOW_SUCCESS') {
    if (action.follows.length === 0) {
      return null
    }
    const follow = action.follows[0]
    const xfollows = state.slice()
    const index = xfollows.findIndex(f => f.entity_id === action.entityID)
    if (index > -1) {
      xfollows[index] = follow
    } else {
      xfollows.push(follow)
    }
    return xfollows
  }
  if (action.type === 'FOLLOW_SUCCESS') {
    const xfollows = state.slice()
    xfollows.push(action.follow)
    return xfollows
  }
  if (action.type === 'UNFOLLOW_SUCCESS') {
    const xfollows = state.slice()
    const i = xfollows.findIndex(follow => follow.id === action.id)
    xfollows.splice(i, 1)
    return xfollows
  }
  return state
}
