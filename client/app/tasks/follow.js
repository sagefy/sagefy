const store = require('../modules/store')
const tasks = require('../modules/tasks')

const recorder = require('../modules/recorder')

const request = require('../modules/request')

module.exports = tasks.add({
    listFollows: (skip = 0, limit = 50) => {
        recorder.emit('list follows')
        return request({
            method: 'GET',
            url: '/s/follows',
            data: {skip, limit, entities: true},
        })
            .then((response) => {
                store.dispatch({
                    type: 'LIST_FOLLOWS_SUCCESS',
                    follows: response.follows,
                    entities: response.entities,
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'list follows failure',
                    errors,
                })
            })
    },

    askFollow: (entityID) => {
        recorder.emit('ask follow', entityID)
        return request({
            method: 'GET',
            url: '/s/follows',
            data: {entity_id: entityID},
        })
            .then((response) => {
                store.dispatch({
                    type: 'ASK_FOLLOW_SUCCESS',
                    follows: response.follows,
                    entityID
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'ask follow failure',
                    errors,
                })
            })
    },

    follow: (data) => {
        recorder.emit('follow', data.entity.id)
        return request({
            method: 'POST',
            url: '/s/follows',
            data: data,
        })
            .then((response) => {
                store.dispatch({
                    type: 'FOLLOW_SUCCESS',
                    follow: response.follow
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'follow failure',
                    errors,
                })
            })
    },

    unfollow: (id) => {
        recorder.emit('unfollow', id)
        return request({
            method: 'DELETE',
            url: `/s/follows/${id}`,
        })
            .then(() => {
                store.dispatch({
                    type: 'UNFOLLOW_SUCCESS',
                    id
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'unfollow failure',
                    errors,
                })
            })
    }
})
