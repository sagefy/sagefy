/* eslint-disable camelcase */
const {dispatch} = require('../modules/store')
const tasks = require('../modules/tasks')
const request = require('../modules/request')

module.exports = tasks.add({
    listPosts(id) {
        dispatch({type: 'LIST_POSTS', id})
        return request({
            method: 'GET',
            url: `/s/topics/${id}/posts`,
            data: {},
        })
            .then((response) => {
                dispatch({
                    type: 'ADD_TOPIC',
                    topic: response.topic,
                    id,
                })

                const posts = response.posts
                posts.forEach(post => {
                    const user = response.users[post.user_id]
                    post.user_name = user.name
                    post.user_avatar = user.avatar
                    if (!response.entity_versions) { return }
                    const entityVersions = response.entity_versions[post.id]
                    if (entityVersions) {
                        post.entityVersionsFull =
                        entityVersions.map((data, index) => {
                            return Object.assign({}, data, {
                                entityKind: post.entity_versions[index].kind,
                            })
                        })
                    }
                })

                dispatch({
                    type: 'ADD_TOPIC_POSTS',
                    message: 'list posts success',
                    topic_id: id,
                    posts,
                })

                if ('card' in response) {
                    dispatch({
                        type: 'LIST_POSTS_SUCCESS',
                        entity: 'card',
                        card: response.card,
                    })
                } else if ('unit' in response) {
                    dispatch({
                        type: 'ADD_UNIT',
                        unit: response.unit,
                    })
                } else if ('subject' in response) {
                    dispatch({
                        type: 'ADD_SUBJECT',
                        subject: response.subject,
                    })
                }
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
            type: 'SET_SENDING_ON'
        })
        const topicId = data.post.topicId || data.post.topic_id
        dispatch({type: 'CREATE_POST', topicId})
        return request({
            method: 'POST',
            url: `/s/topics/${topicId}/posts`,
            data: data,
        })
            .then((response) => {
                dispatch({
                    type: 'ADD_TOPIC_POSTS',
                    message: 'create post success',
                    topic_id: topicId,
                    posts: [response.post],
                })
                tasks.route(`/topics/${topicId}`)
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'create post failure',
                    errors,
                })
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    },

    updatePost(data) {
        dispatch({
            type: 'SET_SENDING_ON'
        })
        const {id} = data.post
        const topicId = data.post.topic_id
        dispatch({type: 'UPDATE_POST'})
        return request({
            method: 'PUT',
            url: `/s/topics/${topicId}/posts/${id}`,
            data: data,
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
                    type: 'SET_SENDING_OFF'
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'update post failure',
                    errors,
                })
                dispatch({
                    type: 'SET_SENDING_OFF'
                })
            })
    }
})
