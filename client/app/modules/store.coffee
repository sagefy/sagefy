module.exports = {
    data: window.preload or {}
    tasks: {}

    init: (fn) ->
        fn.call(this)

    add: (obj) ->
        @tasks[key] = fn.bind(this) for key, fn of obj
        return obj

    bind: (fn) ->
        return @callback = fn

    change: ->
        return @callback(@data) if @callback
}
