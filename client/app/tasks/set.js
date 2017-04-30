const {dispatch} = require('../modules/store')
const tasks = require('../modules/tasks')
const {matchesRoute} = require('../modules/auxiliaries')
const request = require('../modules/request')

module.exports = tasks.add({
    getSet(id) {
        dispatch({type: 'GET_SET', id})
        return request({
            method: 'GET',
            url: `/s/sets/${id}`,
            data: {},
        })
            .then((response) => {
                const set = response.set
                ;['topics', 'versions', 'units'].forEach(r => {
                    set[r] = response[r]
                })
                dispatch({
                    type: 'ADD_SET',
                    message: 'get set success',
                    set,
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'get set failure',
                    errors,
                })
            })
    },

    getRecommendedSets() {
        dispatch({type: 'GET_RECOMMENDED_SETS'})
        return request({
            method: 'GET',
            url: '/s/sets/recommended',
            data: {},
        })
            .then((response) => {
                dispatch({
                    type: 'SET_RECOMMENDED_SETS',
                    message: 'get recommended sets success',
                    recommendedSets: response.sets,
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'get recommended sets failure',
                    errors,
                })
            })
    },

    listSetVersions(id) {
        dispatch({type: 'LIST_SET_VERSIONS', id})
        return request({
            method: 'GET',
            url: `/s/sets/${id}/versions`,
            data: {},
        })
            .then((response) => {
                dispatch({
                    type: 'ADD_SET_VERSIONS',
                    versions: response.versions,
                    entity_id: id,
                    message: 'list set versions success',
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'list set versions failure',
                    errors,
                })
            })
    },

    getSetTree(id) {
        dispatch({type: 'GET_SET_TREE', id})
        return request({
            method: 'GET',
            url: `/s/sets/${id}/tree`,
            data: {},
        })
            .then((response) => {
                dispatch({
                    type: 'ADD_SET_TREE',
                    message: 'get set tree success',
                    tree: response,
                    id,
                })
                if (response.next && response.next.path) {
                    dispatch({
                        type: 'SET_NEXT',
                        next: response.next,
                    })
                }
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'get set tree failure',
                    errors,
                })
            })
    },

    selectTreeUnit(id) {
        dispatch({
            type: 'SET_CURRENT_TREE_UNIT',
            id,
        })
    },

    getSetUnits(id) {
        dispatch({type: 'GET_SET_UNITS', id})
        return request({
            method: 'GET',
            url: `/s/sets/${id}/units`,
            data: {},
        })
            .then((response) => {
                dispatch({
                    type: 'SET_CHOOSE_UNIT',
                    chooseUnit: response,
                    message: 'get set units success',
                })
                dispatch({
                    type: 'SET_NEXT',
                    next: response.next,
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'get set units failure',
                    errors,
                })
            })
    },

    chooseUnit(setId, unitId) {
        dispatch({type: 'CHOOSE_UNIT', setId, unitId})
        return request({
            method: 'POST',
            url: `/s/sets/${setId}/units/${unitId}`,
            data: {},
        })
            .then((response) => {
                dispatch({type: 'CHOOSE_UNIT_SUCCESS', setId, unitId})
                const {next} = response
                dispatch({
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
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'choose unit failure',
                    errors,
                })
            })
    }
})
