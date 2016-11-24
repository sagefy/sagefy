const store = require('../modules/store')
const tasks = require('../modules/tasks')

const recorder = require('../modules/recorder')
const {mergeArraysByKey} = require('../modules/auxiliaries')
const errorsReducer = require('../reducers/errors')

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
                store.data.units = store.data.units || {}
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
                store.data.units[id] = unit
                recorder.emit('get unit success', id)
                store.change()
            })
            .catch((errors) => {
                store.update('errors', errorsReducer, {
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
                store.data.unitVersions = store.data.unitVersions || {}
                store.data.unitVersions[id] = store.data.unitVersions[id] || []
                store.data.unitVersions[id] = mergeArraysByKey(
                    store.data.unitVersions[id],
                    response.versions,
                    'id'
                )
                recorder.emit('list unit versions success', id)
                store.change()
            })
            .catch((errors) => {
                store.update('errors', errorsReducer, {
                    type: 'SET_ERRORS',
                    message: 'list unit versions failure',
                    errors,
                })
            })
    }
})
