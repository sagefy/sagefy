const store = require('../modules/store')
const tasks = require('../modules/tasks')
const recorder = require('../modules/recorder')
const {matchesRoute} = require('../modules/auxiliaries')
const request = require('../modules/request')

module.exports = tasks.add({
    getSet: (id) => {
        recorder.emit('get set', id)
        return request({
            method: 'GET',
            url: `/s/sets/${id}`,
            data: {},
        })
            .then((response) => {
                const set = response.set
                store.data.sets = store.data.sets || {}
                store.data.sets[id] = set
                ;['topics', 'versions', 'units'].forEach(r => {
                    set[r] = response[r]
                })
                recorder.emit('get set success', id)
                store.change()
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'get set failure',
                    errors,
                })
            })
    },

    getRecommendedSets: () => {
        recorder.emit('get recommended sets')
        return request({
            method: 'GET',
            url: '/s/sets/recommended',
            data: {},
        })
            .then((response) => {
                store.data.recommendedSets = response.sets
                recorder.emit('get recommended sets success')
                store.change()
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'get recommended sets failure',
                    errors,
                })
            })
    },

    listSetVersions: (id) => {
        recorder.emit('list set versions', id)
        return request({
            method: 'GET',
            url: `/s/sets/${id}/versions`,
            data: {},
        })
            .then((response) => {
                store.dispatch({
                    type: 'ADD_SET_VERSIONS',
                    versions: response.versions,
                    entity_id: id,
                    message: 'list set versions success',
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'list set versions failure',
                    errors,
                })
            })
    },

    getSetTree: (id) => {
        recorder.emit('get set tree', id)
        return request({
            method: 'GET',
            url: `/s/sets/${id}/tree`,
            data: {},
        })
            .then((response) => {
                store.data.setTrees = store.data.setTrees || {}
                store.data.setTrees[id] = response
                recorder.emit('get set tree success', id)
                if (response.next && response.next.path) {
                    store.dispatch({
                        type: 'SET_NEXT',
                        next: response.next,
                    })
                }
                store.change()
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'get set tree failure',
                    errors,
                })
            })
    },

    selectTreeUnit: (id) => {
        store.dispatch({
            type: 'SET_CURRENT_TREE_UNIT',
            id,
        })
    },

    getSetUnits: (id) => {
        recorder.emit('get set units', id)
        return request({
            method: 'GET',
            url: `/s/sets/${id}/units`,
            data: {},
        })
            .then((response) => {
                store.dispatch({
                    type: 'SET_CHOOSE_UNIT',
                    chooseUnit: response,
                    message: 'get set units success',
                })
                store.dispatch({
                    type: 'SET_NEXT',
                    next: response.next,
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'get set units failure',
                    errors,
                })
            })
    },

    chooseUnit: (setId, unitId) => {
        recorder.emit('choose unit', setId, unitId)
        return request({
            method: 'POST',
            url: `/s/sets/${setId}/units/${unitId}`,
            data: {},
        })
            .then((response) => {
                recorder.emit('choose unit success', setId, unitId)
                const {next} = response
                store.dispatch({
                    type: 'SET_NEXT',
                    next,
                })
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
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'choose unit failure',
                    errors,
                })
            })
    }
})
