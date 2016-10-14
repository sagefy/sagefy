const store = require('../modules/store')
const ajax = require('../modules/ajax').ajax
const recorder = require('../modules/recorder')
const {mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
    getUnit: (id) => {
        recorder.emit('get unit', id)
        ajax({
            method: 'GET',
            url: `/s/units/${id}`,
            data: {},
            done: (response) => {
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
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('get unit failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    },

    listUnitVersions: (id) => {
        recorder.emit('list unit versions', id)
        ajax({
            method: 'GET',
            url: `/s/units/${id}/versions`,
            data: {},
            done: (response) => {
                store.data.unitVersions = store.data.unitVersions || {}
                store.data.unitVersions[id] = store.data.unitVersions[id] || []
                store.data.unitVersions[id] = mergeArraysByKey(
                    store.data.unitVersions[id],
                    response.versions,
                    'id'
                )
                recorder.emit('list unit versions success', id)
            },
            fail: (errors) => {
                store.data.errors = errors
                recorder.emit('list unit versions failure', errors)
            },
            always: () => {
                store.change()
            }
        })
    }
})
