module.exports = {
    data: window.preload or {}
    actions: {}

    init: (fn) ->
        fn.call(this)

    add: (obj) ->
        for key, fn of obj
            @actions[key] = fn.bind(this)
        return obj

    bind: (fn) ->
        return @callback = fn

    change: ->
        return @callback(@data)
}
