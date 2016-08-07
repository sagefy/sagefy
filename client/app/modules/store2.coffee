# TODO-2 try to load the state from local storage.
# BUT if there's no cookie, then act like local storage isn't there.
# Also, state changes should update the data in local storage as well.

listeners = []
state = window.preload or {}
reducer = ->

module.exports = {
    setReducer: (fn) ->
        reducer = fn

    subscribe: (listener) ->
        listeners.push(listener)
        return unsubscribe = ->
            index = listeners.indexOf(listener)
            listeners.splice(index, 1) if index > -1

    dispatch: (action) ->
        state = reducer(state, action)
        listeners.forEach((listener) -> listener(state, action))
        return action
}
