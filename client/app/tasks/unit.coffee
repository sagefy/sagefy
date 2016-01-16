store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
{mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
    getUnit: (id) ->
        recorder.emit('get unit', id)
        ajax({
            method: 'GET'
            url: "/s/units/#{id}"
            data: {}
            done: (response) =>
                @data.units ?= {}
                unit = response.unit
                ['topics', 'versions'].forEach((r) ->
                    unit[r] = response[r]
                )
                unit.relationships = []
                ['belongs_to', 'requires', 'required_by'].forEach((r) ->
                    response[r].forEach((e) ->
                        unit.relationships.push({
                            kind: r
                            entity: e
                        })
                    )
                )
                @data.units[id] = unit
                recorder.emit('get unit success', id)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('get unit failure', errors)
            always: =>
                @change()
        })

    listUnitVersions: (id) ->
        recorder.emit('list unit versions', id)
        ajax({
            method: 'GET'
            url: "/s/units/#{id}/versions"
            data: {}
            done: (response) =>
                @data.unitVersions ?= {}
                @data.unitVersions[id] ?= []
                @data.unitVersions[id] = mergeArraysByKey(
                    @data.unitVersions[id]
                    response.versions
                    'id'
                )
                recorder.emit('list unit versions success', id)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('list unit versions failure', errors)
            always: =>
                @change()
        })
})
