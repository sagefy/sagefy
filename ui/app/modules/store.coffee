module.exports = {
    data: window.preload or {}
    actions: {}

    init: (fn) ->
        fn.call(this)

    add: (obj) ->
        @actions[key] = fn.bind(this) for key, fn of obj
        return obj

    bind: (fn) ->
        return @callback = fn

    change: ->
        return @callback(@data)
}
