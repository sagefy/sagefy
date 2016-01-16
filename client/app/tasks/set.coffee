store = require('../modules/store')
ajax = require('../modules/ajax').ajax
recorder = require('../modules/recorder')
{matchesRoute} = require('../modules/auxiliaries')
{mergeArraysByKey} = require('../modules/auxiliaries')

module.exports = store.add({
    getSet: (id) ->
        recorder.emit('get set', id)
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
                recorder.emit('get set success', id)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('get set failure', errors)
            always: =>
                @change()
        })

    listSetVersions: (id) ->
        recorder.emit('list set versions', id)
        ajax({
            method: 'GET'
            url: "/s/sets/#{id}/versions"
            data: {}
            done: (response) =>
                @data.setVersions ?= {}
                @data.setVersions[id] ?= []
                @data.setVersions[id] = mergeArraysByKey(
                    @data.setVersions[id]
                    response.versions
                    'id'
                )
                recorder.emit('list set versions success', id)
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('list set versions failure', errors)
            always: =>
                @change()
        })

    getSetTree: (id) ->
        recorder.emit('get set tree', id)
        ajax({
            method: 'GET'
            url: "/s/sets/#{id}/tree"
            data: {}
            done: (response) =>
                @data.setTrees ?= {}
                @data.setTrees[id] = response
                recorder.emit('get set tree success', id)
                if response.next?.path
                    recorder.emit('next', response.next)
                    @data.next = response.next
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('get set tree failure', errors)
            always: =>
                @change()
        })

    selectTreeUnit: (id) ->
        recorder.emit('select tree unit', id)
        @data.currentTreeUnit = id
        @change()

    getSetUnits: (id) ->
        recorder.emit('get set units', id)
        ajax({
            method: 'GET'
            url: "/s/sets/#{id}/units"
            data: {}
            done: (response) =>
                @data.chooseUnit = response
                recorder.emit('get set units success', id)
                recorder.emit('next', response.next)
                @data.next = response.next
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('get set units failure', errors)
            always: =>
                @change()
        })

    chooseUnit: (setId, unitId) ->
        recorder.emit('choose unit', setId, unitId)
        ajax({
            method: 'POST'
            url: "/s/sets/#{setId}/units/#{unitId}"
            data: {}
            done: (response) =>
                recorder.emit('choose unit success', setId, unitId)
                {next} = response
                @data.next = next
                recorder.emit('next', next)
                @tasks.updateMenuContext({
                    set: setId
                    unit: unitId
                    card: false
                })
                if args = matchesRoute(next.path, '/s/cards/{id}/learn')
                    @tasks.route("/cards/#{args[0]}/learn")
            fail: (errors) =>
                @data.errors = errors
                recorder.emit('choose unit failure', errors)
            always: =>
                @change()
        })
})
