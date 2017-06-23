/* eslint-disable camelcase */
const { dispatch } = require('../modules/store')
const tasks = require('../modules/tasks')
const request = require('../modules/request')

function flatten(arr) {
    return arr.reduce(
        (acc, val) => acc.concat(
            Array.isArray(val) ? flatten(val) : val
        ),
        []
    )
}

module.exports = tasks.add({
    listPostsForTopic(id) {
        return tasks.listPosts(id)
            .then((response) => {
                const userIds = response.posts.map(post => post.user_id)
                const entityVersions = flatten(response.posts
                    .filter(post => post.kind === 'proposal')
                    .map(post => post.entity_versions))
                return Promise.all([
                    tasks.getTopic(id)
                        .then((response) => {
                            const kind = response.topic.entity.kind
                            const entityId = response.topic.entity.id
                            return tasks.getEntity(kind, entityId)
                        }),
                    tasks.listUsers(userIds, { size: 48 }),
                    tasks.listEntityVersionsByTopic(id, entityVersions),
                ])
            })
    },

    listPosts(id) {
        dispatch({ type: 'LIST_POSTS', id })
        return request({
            method: 'GET',
            url: `/s/topics/${id}/posts`,
            data: {},
        })
            .then((response) => {
                const posts = response.posts
                dispatch({
                    type: 'ADD_TOPIC_POSTS',
                    message: 'list posts success',
                    topic_id: id,
                    posts,
                })
                return response
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'list posts failure',
                    errors,
                })
            })
    },

    createPost(data) {
        dispatch({
            type: 'SET_SENDING_ON',
        })
        const topicId = data.post.topicId || data.post.topic_id
        dispatch({ type: 'CREATE_POST', topicId })
        return request({
            method: 'POST',
            url: `/s/topics/${topicId}/posts`,
            data: data.post,
        })
            .then((response) => {
                dispatch({
                    type: 'ADD_TOPIC_POSTS',
                    message: 'create post success',
                    topic_id: topicId,
                    posts: [response.post],
                })
                dispatch({
                    type: 'SET_SENDING_OFF',
                })
                tasks.route(`/topics/${topicId}`)
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'create post failure',
                    errors,
                })
                dispatch({
                    type: 'SET_SENDING_OFF',
                })
            })
    },

    updatePost(data) {
        dispatch({
            type: 'SET_SENDING_ON',
        })
        const { id } = data.post
        const topicId = data.post.topic_id
        dispatch({ type: 'UPDATE_POST' })
        return request({
            method: 'PUT',
            url: `/s/topics/${topicId}/posts/${id}`,
            data: data.post,
        })
            .then((response) => {
                dispatch({
                    type: 'UPDATE_POST_SUCCESS',
                    topicId,
                    postId: id,
                    post: response.post,
                })
                tasks.route(`/topics/${topicId}`)
                dispatch({
                    type: 'SET_SENDING_OFF',
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'update post failure',
                    errors,
                })
                dispatch({
                    type: 'SET_SENDING_OFF',
                })
            })
    },
})
