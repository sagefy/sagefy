const store = require('../modules/store')
const tasks = require('../modules/tasks')
const recorder = require('../modules/recorder')
const request = require('../modules/request')

module.exports = tasks.add({
    getUnit: (id) => {
        recorder.emit('get unit', id)
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
                store.dispatch({
                    type: 'ADD_UNIT',
                    message: 'get unit success',
                    unit,
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'get unit failure',
                    errors,
                })
            })
    },

    listUnitVersions: (id) => {
        recorder.emit('list unit versions', id)
        return request({
            method: 'GET',
            url: `/s/units/${id}/versions`,
            data: {},
        })
            .then((response) => {
                store.dispatch({
                    type: 'ADD_UNIT_VERSIONS',
                    versions: response.versions,
                    entity_id: id,
                    message: 'list unit versions success',
                })
            })
            .catch((errors) => {
                store.dispatch({
                    type: 'SET_ERRORS',
                    message: 'list unit versions failure',
                    errors,
                })
            })
    }
})
