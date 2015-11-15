store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')

module.exports = store.add({
    getSet: (id) ->
        ajax({
            method: 'GET'
            url: "/s/sets/#{id}"
            data: {}
            done: (response) =>
                set = response.set
                @data.sets ?= {}
                @data.sets[id] = set
                ['topics', 'versions', 'units'].forEach((r) ->
                    set[r] = response[r]
                )
                recorder.emit('get set')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on get set', errors)
            always: =>
                @change()
        })

    listSetVersions: (id) ->
        ajax({
            method: 'GET'
            url: "/s/sets/#{id}/versions"
            data: {}
            done: (response) =>
                @data.setVersions ?= {}
                # TODO merge based on id and created
                @data.setVersions[id] = response.versions
                recorder.emit('list set versions')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on list set versions', errors)
            always: =>
                @change()
        })

    getSetTree: (id) ->
        ajax({
            method: 'GET'
            url: '/s/sets/{set_id}/tree'
            data: {}
            done: (response) =>
                # @data
                recorder.emit('get set tree')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on get set tree', errors)
            always: =>
                @change()
        })

    getSetUnits: (id) ->
        ajax({
            method: 'GET'
            url: "/s/sets/#{id}/units"
            data: {}
            done: (response) =>
                @data.trees ?= {}
                @data.trees[id] = response.set
                recorder.emit('get set units')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on get set units', errors)
            always: =>
                @change()
        })

    chooseUnit: (setId, unitId) ->
        ajax({
            method: 'POST'
            url: "/s/sets/#{setId}/units/#{unitId}"
            data: {}
            done: (response) =>
                # @data TODO
                recorder.emit('choose unit')
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('error on choose unit', errors)
            always: =>
                @change()
        })
})
