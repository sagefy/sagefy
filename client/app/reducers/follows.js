const {extend} = require('../modules/utilities')
const {mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = function follows(state = [], action = {type: ''}) {
    if(action.type === 'LIST_FOLLOWS_SUCCESS') {
        const follows = mergeArraysByKey(
            state,
            action.follows,
            'id'
        )
        follows.forEach((follow, i) => {
            extend(follow.entity, action.entities[i])
        })
        return follows
    }
    if(action.type === 'ASK_FOLLOW_SUCCESS') {
        if (action.follows.length === 0) { return }
        const follow = action.follows[0]
        const follows = state
        const index = follows.findIndex((f) =>
            f.entity.id === action.entityID)
        if (index > -1) {
            follows[index] = follow
        } else {
            follows.push(follow)
        }
        return follows
        // TODO-3 will this cause a bug with mergeArraysByKey later?
    }
    if(action.type === 'FOLLOW_SUCCESS') {
        const follows = state
        follows.push(action.follow)
        return follows
        // TODO-3 will this cause a bug with mergeArraysByKey later?
    }
    if(action.type === 'UNFOLLOW_SUCCESS') {
        const follows = state
        const i = follows.findIndex((follow) =>
            follow.id === action.id)
        follows.splice(i, 1)
        return follows
    }
    return state
}
