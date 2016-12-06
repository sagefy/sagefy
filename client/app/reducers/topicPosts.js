const {shallowCopy} = require('../modules/utilities')
const {mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = function topicPosts(state = {}, action = {type: ''}) {
    if(action.type === 'ADD_TOPIC_POSTS') {
        state = shallowCopy(state)
        let posts = state[action.topic_id] || []
        posts = mergeArraysByKey(
            posts,
            action.posts,
            'id'
        )
        state[action.topic_id] = posts
        return state
    }
    return state
}
