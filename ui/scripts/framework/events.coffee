###
A class which defines and manages the events system.
Designed to be extended.
###

class Events
    # Establishes the events and listeners hashes
    # Descending classes should call `super` before defining their own
    constructor: (@options = {}) ->
        @events = {}
        @listeners = []

    # Descending objects should super this method
    remove: ->
        @stopListening()
        @off()
        return this

    # Triggers the event, where `name` is a string, and `args` will
    # be passed to any event handlers
    trigger: (name, args...) ->
        if @events[name]
            for fn in @events[name]
                fn.apply(this, args)
        return this

    # Bind to events
    # If arguments are `name` (string) and `fn` (function)
    # then it will add it to the functions to be called on `name`
    on: (name, fn) ->
        @events[name] ||= []

        # Ensure this function isn't already added before adding it
        if @events[name].indexOf(fn) is -1
            @events[name].push(fn)

        return this

    # Removes events
    off: (name, fn) ->
        # If a name and function is provided, it will remove that function
        if name and @events[name] and fn
            index = @events[name].indexOf(fn)
            if index > -1
                @events[name].splice(index, 1)

        # If only name is provided, all events under that name are removed
        else if name
            @events[name] = []

        # If no name is provided, it removes all events
        else
            @events = {}

        return this

    # Keep track of when this object listens to events on other objects
    listenTo: (obj, name, fn) ->
        @listeners.push({obj: obj, name: name, fn: fn})
        obj.on(name, fn)
        return this

    # Removes listeners
    # Argument is an options object, with keys `obj`, `name`, and `fn`
    stopListening: (opts = {}) ->
        # If no options are provided, then remove all listeners
        if not opts
            @listeners = []
            return this

        # Find listeners matching the criteria and remove them
        for index, listener of @listeners.slice()
            matches = true
            for key, value of opts
                if listener[key] isnt value
                    matches = false
            if matches
                listener.obj.off(listener.name, listener.fn)
                @listeners.splice(index, 1)

        return this

module.exports = Events
