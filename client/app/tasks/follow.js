const store = require('../modules/store')
const tasks = require('../modules/tasks')
const request = require('../modules/request')
const recorder = require('../modules/recorder')
const errorsReducer = require('../reducers/errors')
const followsReducer = require('../reducers/follows')

module.exports = tasks.add({
    listFollows: (skip = 0, limit = 50) => {
        recorder.emit('list follows')
        request({
            method: 'GET',
            url: '/s/follows',
            data: {skip, limit, entities: true},
            done: (response) => {
                store.update('follows', followsReducer, {
                    type: 'LIST_FOLLOWS_SUCCESS',
                    follows: response.follows,
                    entities: response.entities,
                })
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'list follows failure',
                    errors,
                })
            }
        })
    },

    askFollow: (entityID) => {
        recorder.emit('ask follow', entityID)
        request({
            method: 'GET',
            url: '/s/follows',
            data: {entity_id: entityID},
            done: (response) => {
                store.update('follows', followsReducer, {
                    type: 'ASK_FOLLOW_SUCCESS',
                    follows: response.follows,
                    entityID
                })
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'ask follow failure',
                    errors,
                })
            }
        })
    },

    follow: (data) => {
        recorder.emit('follow', data.entity.id)
        request({
            method: 'POST',
            url: '/s/follows',
            data: data,
            done: (response) => {
                store.update('follows', followsReducer, {
                    type: 'FOLLOW_SUCCESS',
                    follow: response.follow
                })
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'follow failure',
                    errors,
                })
            }
        })
    },

    unfollow: (id) => {
        recorder.emit('unfollow', id)
        request({
            method: 'DELETE',
            url: `/s/follows/${id}`,
            done: () => {
                store.update('follows', followsReducer, {
                    type: 'UNFOLLOW_SUCCESS',
                    id
                })
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'unfollow failure',
                    errors,
                })
            }
        })
    }
})
