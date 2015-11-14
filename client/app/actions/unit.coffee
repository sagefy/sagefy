store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')

module.exports = store.add({
    getUnit: (id) ->
        ajax({
            method: 'GET'
            url: "/s/units/#{id}"
            data: {}
            done: (response) =>
                @data.units ?= {}
                unit = response.unit
                ['topics', 'versions'].forEach((r) -> unit[r] = response[r])
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
                recorder.emit('get unit')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on get unit', errors)
            always: =>
                @change()
        })

    listUnitVersion: (id) ->
        ajax({
            method: 'GET'
            url: "/s/units/#{id}/versions"
            data: {}
            done: (response) =>
                @data.unitVersions ?= {}
                @data.unitVersions[id] ?= []
                # TODO merge based on id and created
                @data.unitVersions[id] = response.versions
                recorder.emit('list unit version')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on list unit version', errors)
            always: =>
                @change()
        })
})
