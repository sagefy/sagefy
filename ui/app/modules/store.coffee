module.exports = {
    data: window.preload or {}
    actions: {}

    init: (fn) ->
        fn.call(this)

    add: (obj) ->
        for key, value of obj
            @actions[key] = value
        return obj

    bind: (fn) ->
        return @callback = fn

    change: ->
        return @callback(@data)
}
