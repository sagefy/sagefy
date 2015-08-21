require('matches_polyfill')
diff = require('virtual-dom/diff')
patch = require('virtual-dom/patch')
createElement = require('virtual-dom/create-element')

module.exports = {
    events: {}

    init: (fn) ->
        fn.call(this)

    add: (obj) ->
        for query, fn of obj
            match = query.match(eventRegExp)
            type = if match then match[1] else query
            selector = if match then match[2] else ''
            @events[type][selector] = fn
        return obj

    delegate: (type) ->
        return (e) =>
            el = e.currentTarget
            loop
                for selector, fn of @events[type]
                    if el.matches(selector)
                        fn.call(this, e, el)
                        return
                el = el.parentNode
                return if el is @el
}
