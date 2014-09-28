###
One-off functions that are used throughout the framework.
###

Element.prototype.matches = Element.prototype.matches or
                            Element.prototype.matchesSelector or
                            Element.prototype.mozMatchesSelector or
                            Element.prototype.webkitMatchesSelector or
                            Element.prototype.oMatchesSelector or
                            Element.prototype.msMatchesSelector

_ = {}

[
    'Object'
    'Array'
    'Function'
    'Date'
    'String'
    'RegExp'
].forEach((type) ->
    _['is' + type] = (a) ->
        return Object::toString.call(a) is '[object ' + type + ']'
)

_.isUndefined = (a) ->
    return typeof a is "undefined"

_.extend = (target, injects...) ->
    for inject in injects
        for prop, val of inject
            if _.isUndefined(val)
                continue
            target[prop] = switch
                when _.isDate(val)
                    new Date(val)
                when _.isArray(val)
                    target[prop] = [] unless _.isArray(target[prop])
                    _.extend(target[prop], val)
                when _.isObject(val)
                    target[prop] = {} unless _.isObject(target[prop])
                    _.extend(target[prop], val)
                else val # number, boolean, string, regexp, null, function
    return target

# Try to parse a string as JSON
# Otherwise just return the string
_.parseJSON = (str) ->
    try
        return JSON.parse(str)
    catch e
        return str

# Find the closest element matching the given selector
_.closest = (element, top, selector) ->
    while not element.matches(selector)
        element = element.parentNode
        if element is top
            return null
    return element

# Wait for function to stop being called for `delay`
# milliseconds, and then finally call the real function.
_.debounce = (fn, delay) ->
    timer = null
    return (args...) ->
        clearTimeout(timer)
        timer = setTimeout(=>
            fn.apply(this, args)
        , delay)

module.exports = _
