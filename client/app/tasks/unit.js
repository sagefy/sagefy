const { dispatch } = require('../modules/store')
const tasks = require('../modules/tasks')
const request = require('../modules/request')

module.exports = tasks.add({
    getUnit(id) {
        dispatch({ type: 'GET_UNIT', id })
        return request({
            method: 'GET',
            url: `/s/units/${id}`,
            data: {},
        })
            .then((response) => {
                const unit = response.unit
                unit.relationships = []
                ;['belongs_to', 'requires', 'required_by'].forEach(r =>
                    response[r].forEach(e =>
                        unit.relationships.push({
                            kind: r,
                            entity: e,
                        })
                    )
                )
                dispatch({
                    type: 'ADD_UNIT',
                    message: 'get unit success',
                    unit,
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'get unit failure',
                    errors,
                })
            })
    },

    listUnitVersions(id) {
        dispatch({ type: 'LIST_UNIT_VERSIONS', id })
        return request({
            method: 'GET',
            url: `/s/units/${id}/versions`,
            data: {},
        })
            .then((response) => {
                dispatch({
                    type: 'ADD_UNIT_VERSIONS',
                    versions: response.versions,
                    entity_id: id,
                    message: 'list unit versions success',
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'list unit versions failure',
                    errors,
                })
            })
    },

    createNewUnitVersions(units) {
        let count = 0
        const total = units.length
        const allResponses = []
        return new Promise((resolve, reject) => {
            units.forEach((unit) => {
                request({
                    method: 'POST',
                    url: '/s/units/versions',
                    data: unit,
                })
                    .then((response) => {
                        allResponses.push(response.version)
                        count++
                        if (count === total) {
                            resolve({ units: allResponses })
                        }
                    })
                    .catch((errors) => {
                        dispatch({
                            type: 'SET_ERRORS',
                            message: 'create new unit version failure',
                            errors,
                        })
                        reject()
                    })
            })
        })
    },

    getMyRecentUnits() {
        dispatch({ type: 'GET_MY_RECENT_UNITS' })
        return request({
            method: 'GET',
            url: '/s/units:get_my_recently_created',
            data: {},
        })
            .then((response) => {
                dispatch({
                    type: 'SET_MY_RECENT_UNITS',
                    units: response.units,
                })
            })
            .catch((errors) => {
                dispatch({
                    type: 'SET_ERRORS',
                    message: 'get my recent units failure',
                    errors,
                })
            })
    },
})
