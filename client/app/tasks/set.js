const store = require('../modules/store')
const tasks = require('../modules/tasks')
const ajax = require('../modules/ajax').ajax
const recorder = require('../modules/recorder')
const {matchesRoute} = require('../modules/auxiliaries')
const {mergeArraysByKey} = require('../modules/auxiliaries')
const errorsReducer = require('../reducers/errors')

module.exports = tasks.add({
    getSet: (id) => {
        recorder.emit('get set', id)
        ajax({
            method: 'GET',
            url: `/s/sets/${id}`,
            data: {},
            done: (response) => {
                const set = response.set
                store.data.sets = store.data.sets || {}
                store.data.sets[id] = set
                ;['topics', 'versions', 'units'].forEach(r => {
                    set[r] = response[r]
                })
                recorder.emit('get set success', id)
                store.change()
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'get set failure',
                    errors,
                })
            }
        })
    },

    getRecommendedSets: () => {
        recorder.emit('get recommended sets')
        ajax({
            method: 'GET',
            url: '/s/sets/recommended',
            data: {},
            done: (response) => {
                store.data.recommendedSets = response.sets
                recorder.emit('get recommended sets success')
                store.change()
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'get recommended sets failure',
                    errors,
                })
            }
        })
    },

    listSetVersions: (id) => {
        recorder.emit('list set versions', id)
        ajax({
            method: 'GET',
            url: `/s/sets/${id}/versions`,
            data: {},
            done: (response) => {
                store.data.setVersions = store.data.setVersions || {}
                store.data.setVersions[id] = store.data.setVersions[id] || []
                store.data.setVersions[id] = mergeArraysByKey(
                    store.data.setVersions[id],
                    response.versions,
                    'id'
                )
                recorder.emit('list set versions success', id)
                store.change()
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'list set versions failure',
                    errors,
                })
            }
        })
    },

    getSetTree: (id) => {
        recorder.emit('get set tree', id)
        ajax({
            method: 'GET',
            url: `/s/sets/${id}/tree`,
            data: {},
            done: (response) => {
                store.data.setTrees = store.data.setTrees || {}
                store.data.setTrees[id] = response
                recorder.emit('get set tree success', id)
                if (response.next && response.next.path) {
                    recorder.emit('next', response.next)
                    store.data.next = response.next
                }
                store.change()
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'get set tree failure',
                    errors,
                })
            }
        })
    },

    selectTreeUnit: (id) => {
        recorder.emit('select tree unit', id)
        store.data.currentTreeUnit = id
        store.change()
    },

    getSetUnits: (id) => {
        recorder.emit('get set units', id)
        ajax({
            method: 'GET',
            url: `/s/sets/${id}/units`,
            data: {},
            done: (response) => {
                store.data.chooseUnit = response
                recorder.emit('get set units success', id)
                recorder.emit('next', response.next)
                store.data.next = response.next
                store.change()
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'get set units failure',
                    errors,
                })
            }
        })
    },

    chooseUnit: (setId, unitId) => {
        recorder.emit('choose unit', setId, unitId)
        ajax({
            method: 'POST',
            url: `/s/sets/${setId}/units/${unitId}`,
            data: {},
            done: (response) => {
                recorder.emit('choose unit success', setId, unitId)
                const {next} = response
                store.data.next = next
                recorder.emit('next', next)
                tasks.updateMenuContext({
                    set: setId,
                    unit: unitId,
                    card: false,
                })
                const args = matchesRoute(next.path, '/s/cards/{id}/learn')
                if (args) {
                    tasks.route(`/cards/${args[0]}/learn`)
                }
                store.change()
            },
            fail: (errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'choose unit failure',
                    errors,
                })
            }
        })
    }
})
