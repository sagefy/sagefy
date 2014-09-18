###
One-off functions that are used throughout the framework.
###

Utilities = {}

['Object', 'Array', 'Function', 'Date'].forEach((type) ->
    Utilities['is' + type] = (a) ->
        return Object.prototype.toString.call(a) is '[object ' + type + ']'
)

Utilities.isUndefined = (a) ->
    return typeof a is "undefined"

Utilities.extend = (target, injects...) ->
    for inject in injects
        for prop, val of inject
            if Utilities.isUndefined(val)
                continue
            target[prop] = switch
                when Utilities.isDate(val)
                    new Date(val)
                when Utilities.isArray(val)
                    target[prop] = [] unless Utilities.isArray(target[prop])
                    Utilities.extend(target[prop], val)
                when Utilities.isObject(val)
                    target[prop] = {} unless Utilities.isObject(target[prop])
                    Utilities.extend(target[prop], val)
                else val # number, boolean, string, regexp, null, function
    return target

module.exports = Utilities
