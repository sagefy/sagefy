###
One-off functions that are used throughout the framework.
###

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

module.exports = _
