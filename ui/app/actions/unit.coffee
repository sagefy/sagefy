store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')

module.exports = store.add({
    getUnit: (id) ->
        ajax({
            method: 'GET'
            url: "/api/units/#{id}"
            data: {}
            done: (response) =>
                @data.units ?= {}
                @data.units[id] = response.unit
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
            url: "/api/units/#{id}/versions"
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
