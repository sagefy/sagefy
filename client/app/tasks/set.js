const store = require('../modules/store')
const ajax = require('../modules/ajax').ajax
const recorder = require('../modules/recorder')
const {matchesRoute} = require('../modules/auxiliaries')
const {mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
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
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('get set failure', errors)
            },
            always: () => {
                store.change()
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
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('list set versions failure', errors)
            },
            always: () => {
                store.change()
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
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('get set tree failure', errors)
            },
            always: () => {
                store.change()
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
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('get set units failure', errors)
            },
            always: () => {
                store.change()
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
                store.tasks.updateMenuContext({
                    set: setId,
                    unit: unitId,
                    card: false,
                })
                const args = matchesRoute(next.path, '/s/cards/{id}/learn')
                if (args) {
                    store.tasks.route(`/cards/${args[0]}/learn`)
                }
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('choose unit failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    }
})
