const {dispatch} = require('../modules/store')
const tasks = require('../modules/tasks')
const request = require('../modules/request')

module.exports = tasks.add({
    getUnit: (id) => {
        dispatch({type: 'GET_UNIT', id})
        return request({
            method: 'GET',
            url: `/s/units/${id}`,
            data: {},
        })
            .then((response) => {
                const unit = response.unit
                ;['topics', 'versions'].forEach(r => {
                    unit[r] = response[r]
                })
                unit.relationships = []
                ;['belongs_to', 'requires', 'required_by'].forEach((r) =>
                    response[r].forEach((e) =>
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

    listUnitVersions: (id) => {
        dispatch({type: 'LIST_UNIT_VERSIONS', id})
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
    }
})
