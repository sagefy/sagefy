const store = require('../modules/store')
const ajax = require('../modules/ajax').ajax
const recorder = require('../modules/recorder')
const {extend} = require('../modules/utilities')
const {mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
    listFollows: (skip = 0, limit = 50) => {
        recorder.emit('list follows')
        ajax({
            method: 'GET',
            url: '/s/follows',
            data: {skip, limit, entities: true},
            done: (response) => {
                store.data.follows = store.data.follows || []
                store.data.follows = mergeArraysByKey(
                    store.data.follows,
                    response.follows,
                    'id'
                )
                store.data.follows.forEach((follow, i) => {
                    extend(follow.entity, response.entities[i])
                })
                recorder.emit('list follows success')
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('list follows failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    },

    askFollow: (entityID) => {
        recorder.emit('ask follow', entityID)
        ajax({
            method: 'GET',
            url: '/s/follows',
            data: {entity_id: entityID},
            done: (response) => {
                recorder.emit('ask follow success', entityID)
                if (response.follows.length === 0) { return }
                const follow = response.follows[0]
                store.data.follows = store.data.follows || []
                const index = store.data.follows.findIndex((f) =>
                    f.entity.id === entityID)
                if (index > -1) {
                    store.data.follows[index] = follow
                } else {
                    store.data.follows.push(follow)
                }
                // TODO-3 will this cause a bug with mergeArraysByKey later?
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('ask follow failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    },

    follow: (data) => {
        recorder.emit('follow', data.entity.id)
        ajax({
            method: 'POST',
            url: '/s/follows',
            data: data,
            done: (response) => {
                store.data.follows = store.data.follows || []
                store.data.follows.push(response.follow)
                recorder.emit('follow success', data.entity.id)
                // TODO-3 will this cause a bug with mergeArraysByKey later?
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('follow failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    },

    unfollow: (id) => {
        recorder.emit('unfollow', id)
        ajax({
            method: 'DELETE',
            url: `/s/follows/${id}`,
            done: () => {
                store.data.follows = store.data.follows || []
                const i = store.data.follows.findIndex((follow) =>
                    follow.id === id)
                store.data.follows.splice(i, 1)
                recorder.emit('unfollow success', id)
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('unfollow failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    }
})
