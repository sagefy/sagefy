const { dispatch } = require('../modules/store')
const tasks = require('../modules/tasks')
const request = require('../modules/request')

module.exports = tasks.add({
    listFollows(userId, skip = 0, limit = 50) {
        dispatch({ type: 'LIST_FOLLOWS' })
        return request({
            method: 'GET',
            url: '/s/follows',
            data: { user_id: userId, skip, limit, entities: true },
        })
            .then((response) => {
                dispatch({
                    type: 'LIST_FOLLOWS_SUCCESS',
                    follows: response.follows,
                })
                return tasks.listEntitiesByFollows(response.follows)
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'list follows failure',
                    errors,
                })
            })
    },

    askFollow(entityID) {
        dispatch({ type: 'ASK_FOLLOW', entityID })
        return request({
            method: 'GET',
            url: '/s/follows',
            data: { entity_id: entityID },
        })
            .then((response) => {
                dispatch({
                    type: 'ASK_FOLLOW_SUCCESS',
                    follows: response.follows,
                    entityID,
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'ask follow failure',
                    errors,
                })
            })
    },

    follow(data) {
        dispatch({ type: 'FOLLOW', id: data.entity.id })
        return request({
            method: 'POST',
            url: '/s/follows',
            data: data,
        })
            .then((response) => {
                dispatch({
                    type: 'FOLLOW_SUCCESS',
                    follow: response.follow,
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'follow failure',
                    errors,
                })
            })
    },

    unfollow(id) {
        dispatch({ type: 'UNFOLLOW', id })
        return request({
            method: 'DELETE',
            url: `/s/follows/${id}`,
        })
            .then(() => {
                dispatch({
                    type: 'UNFOLLOW_SUCCESS',
                    id,
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'unfollow failure',
                    errors,
                })
            })
    },
})
