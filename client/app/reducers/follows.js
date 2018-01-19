const { mergeArraysByKey } = require('../modules/auxiliaries')

module.exports = function follows(state = [], action = { type: '' }) {
  if (action.type === 'LIST_FOLLOWS_SUCCESS') {
    const xfollows = mergeArraysByKey(state, action.follows, 'id')
    return xfollows
  }
  if (action.type === 'ASK_FOLLOW_SUCCESS') {
    if (action.follows.length === 0) {
      return null
    }
    const follow = action.follows[0]
    const xfollows = state
    const index = follows.findIndex(f => f.entity_id === action.entityID)
    if (index > -1) {
      follows[index] = follow
    } else {
      follows.push(follow)
    }
    return xfollows
    // TODO-3 will this cause a bug with mergeArraysByKey later?
  }
  if (action.type === 'FOLLOW_SUCCESS') {
    const xfollows = state
    follows.push(action.follow)
    return xfollows
    // TODO-3 will this cause a bug with mergeArraysByKey later?
  }
  if (action.type === 'UNFOLLOW_SUCCESS') {
    const xfollows = state
    const i = follows.findIndex(follow => follow.id === action.id)
    follows.splice(i, 1)
    return xfollows
  }
  return state
}
