const store = require('../modules/store')
const tasks = require('../modules/tasks')

const recorder = require('../modules/recorder')
const {mergeArraysByKey} = require('../modules/auxiliaries')
const errorsReducer = require('../reducers/errors')
const sendingReducer = require('../reducers/sending')
const cardsReducer = require('../reducers/cards')

const request = require('../modules/request')

module.exports = tasks.add({
    listPosts: (id) => {
        recorder.emit('list posts', id)
        return request({
            method: 'GET',
            url: `/s/topics/${id}/posts`,
            data: {},
        })
            .then((response) => {
                store.data.topics = store.data.topics || {}
                store.data.topics[id] = response.topic

                store.data.topicPosts = store.data.topicPosts || {}
                store.data.topicPosts[id] = store.data.topicPosts[id] || []

                const posts = response.posts
                posts.forEach(post => {
                    const user = response.users[post.user_id]
                    post.user_name = user.name
                    post.user_avatar = user.avatar
                    const ev = response.entity_versions[post.id]
                    if (ev) {
                        post.ev = ev
                    }
                })

                store.data.topicPosts[id] = store.data.topicPosts[id] || []
                store.data.topicPosts[id] = mergeArraysByKey(
                    store.data.topicPosts[id],
                    posts,
                    'id'
                )

                if ('card' in response) {
                    store.update('cards', cardsReducer, {
                        type: 'LIST_POSTS_SUCCESS',
                        entity: 'card',
                        card: response.card,
                    })
                } else if ('unit' in response) {
                    store.data.units = store.data.units || {}
                    store.data.units[response.unit.entity_id] = response.unit
                } else if ('set' in response) {
                    store.data.sets = store.data.sets || {}
                    store.data.sets[response.set.entity_id] = response.set
                }

                recorder.emit('list posts success', id)
                store.change()
            })
            .catch((errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'list posts failure',
                    errors,
                })
            })
    },

    createPost: (data) => {
        store.update('sending', sendingReducer, {
            type: 'SET_SENDING_ON'
        })
        const topicId = data.post.topicId
        recorder.emit('create post')
        return request({
            method: 'POST',
            url: `/s/topics/${topicId}/posts`,
            data: data,
        })
            .then((response) => {
                if (store.data.topicPosts && store.data.topicPosts[topicId]) {
                    store.data.topicPosts[topicId].push(response.post)
                }
                recorder.emit('create post success')
                tasks.route(`/topics/${topicId}`)
                store.change()
                store.update('sending', sendingReducer, {
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'create post failure',
                    errors,
                })
                store.update('sending', sendingReducer, {
                    type: 'SET_SENDING_OFF'
                })
            })
    },

    updatePost: (data) => {
        store.update('sending', sendingReducer, {
            type: 'SET_SENDING_ON'
        })
        const {id} = data.post
        const topicId = data.post.topic_id
        recorder.emit('update post')
        return request({
            method: 'PUT',
            url: `/s/topics/${topicId}/posts/${id}`,
            data: data,
        })
            .then((response) => {
                const topic = store.data.topicPosts &&
                              store.data.topicPosts[topicId]
                if (topic) {
                    const index = topic.findIndex((post) => post.id === id)
                    topic[index] = response.post
                }
                recorder.emit('update post success')
                tasks.route(`/topics/${topicId}`)
                store.update('sending', sendingReducer, {
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'update post failure',
                    errors,
                })
                store.update('sending', sendingReducer, {
                    type: 'SET_SENDING_OFF'
                })
            })
    }
})
