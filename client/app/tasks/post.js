const store = require('../modules/store')
const tasks = require('../modules/tasks')
const recorder = require('../modules/recorder')
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
                store.dispatch({
                    type: 'ADD_TOPIC',
                    topic: response.topic,
                    id,
                })

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

                store.dispatch({
                    type: 'ADD_TOPIC_POSTS',
                    message: 'list posts success',
                    topic_id: id,
                    posts,
                })

                if ('card' in response) {
                    store.dispatch({
                        type: 'LIST_POSTS_SUCCESS',
                        entity: 'card',
                        card: response.card,
                    })
                } else if ('unit' in response) {
                    store.dispatch({
                        type: 'ADD_UNIT',
                        unit: response.unit,
                    })
                } else if ('set' in response) {
                    store.dispatch({
                        type: 'ADD_SET',
                        set: response.set,
                    })
                }
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'list posts failure',
                    errors,
                })
            })
    },

    createPost: (data) => {
        store.dispatch({
            type: 'SET_SENDING_ON'
        })
        const topicId = data.post.topicId || data.post.topic_id
        recorder.emit('create post')
        return request({
            method: 'POST',
            url: `/s/topics/${topicId}/posts`,
            data: data,
        })
            .then((response) => {
                store.dispatch({
                    type: 'ADD_TOPIC_POSTS',
                    message: 'create post success',
                    topic_id: topicId,
                    posts: [response.post],
                })
                tasks.route(`/topics/${topicId}`)
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'create post failure',
                    errors,
                })
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    },

    updatePost: (data) => {
        store.dispatch({
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
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'update post failure',
                    errors,
                })
                store.dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    }
})
