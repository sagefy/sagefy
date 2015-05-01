###
A broker is a singleton which defines and manages the events system.
###
broker = {}

# Stores all handlers for all events.
broker.events = events = {}

# Triggers the event, where `name` is a string, and `args` will
# be passed to any handlers.
broker.emit = (name, args...) ->
    if events.all
        broker.emit('all', 'name', args...)
    if events[name]
        for fn in events[name]
            fn.apply(this, args...)
    return this

# Bind to events.
# If arguments are `name` (string) and `fn` (function)
# then it will add it to the functions to be called on `name`.
broker.on = (name, fn) ->
    events[name] ||= []

    # Ensure this function isn't already added before adding it.
    if events[name].indexOf(fn) is -1
        events[name].push(fn)

    return this

# Removes events.
broker.off = (name, fn) ->
    # If a name and function is provided, it will remove that function.
    if name and events[name] and fn
        index = events[name].indexOf(fn)
        if index > -1
            events[name].splice(index, 1)

    # If only name is provided, all events under that name are removed.
    else if name
        events[name] = []

    # If no name is provided, it removes all events.
    else
        events = {}

    return this

module.exports = broker
