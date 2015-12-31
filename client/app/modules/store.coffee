# TODO-2 try to load the state from local storage.
# BUT if there's no cookie, then act like local storage isn't there.
# Also, state changes `change` should update the data in local storage as well.

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
