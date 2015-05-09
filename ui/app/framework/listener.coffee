###
A class that talks to the broker.
Designed to be extended.
###

broker = require('./broker')

class Listener
    constructor: ->
        @listeners = {}

    # Pass along any emit call to the broker.
    emit: (args...) ->
        broker.emit.apply(broker, args)
        return this

    # Keep track of when this object listens to events on the broker.
    on: (name, fn) ->
        @listeners[name] or= []
        @listeners[name].push(fn)
        broker.on(name, fn)
        return this

    # Removes listeners.
    off: (name, fn) ->
        # If a name and function is provided, it will remove that function.
        if name and @listeners[name] and fn
            index = @listeners[name].indexOf(fn)
            if index > -1
                @listeners[name].splice(index, 1)
            broker.off(name, fn)

        # If only name is provided, all events under that name are removed.
        else if name
            broker.off(name, fn) for fn in @listeners[name]
            @listeners[name] = []

        # If no name is provided, it removes all events.
        else
            for name, handlers of @listeners
                broker.off(name, fn) for fn in handlers
            @listeners = {}

        return this

    # On remove, clear out all the listeners.
    remove: ->
        @off()

module.exports = Listener
