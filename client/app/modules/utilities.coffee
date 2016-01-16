###
Utilities are one-off functions that are used throughout the framework.
###
util = {}

# Test for types.
[
    'Object'
    'Array'
    'Function'
    'Date'
    'String'
    'RegExp'
].forEach((type) ->
    util['is' + type] = (a) ->
        return Object::toString.call(a) is '[object ' + type + ']'
)

util.isUndefined = (a) ->
    return typeof a is 'undefined'

objectConstructor = {}.constructor

# Add the properties of the injects into the target.
util.extend = (target, injects...) ->
    for inject in injects
        for prop, val of inject
            if util.isUndefined(val)
                continue
            target[prop] = switch
                when util.isDate(val)
                    new Date(val)
                when util.isArray(val)
                    target[prop] = [] unless util.isArray(target[prop])
                    util.extend([], target[prop], val)
                when (util.isObject(val) and
                      val.constructor is objectConstructor)
                    target[prop] = {} unless util.isObject(target[prop])
                    util.extend({}, target[prop], val)
                else val # number, boolean, string, regexp, null, function
    return target

# Makes a copy of the array or object.
util.copy = (obj) ->
    if util.isObject(obj)
        return util.extend({}, obj)
    if util.isArray(obj)
        return util.extend([], obj)
    if util.isDate(obj)
        return new Date(obj)
    return obj

# Try to parse a string as JSON, otherwise just return the string.
util.parseJSON = (str) ->
    try
        return JSON.parse(str)
    catch e
        return str

# Find the closest element matching the given selector.
require('./matches_polyfill')
util.closest = (element, selector, top = document.body) ->
    while not element.matches(selector)
        element = element.parentNode
        if element is top
            return null
    return element

module.exports = util
