require('./matches_polyfill')

eventRegExp = /^(\S+) (.*)$/

module.exports = {
    events: {
        click: {}
        change: {}
        keydown: {}
        submit: {}
    }

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
            while el isnt @el
                el = if el then el.parentNode else e.currentTarget
                for selector, fn of @events[type]
                    fn.call(this, e, el) if el.matches(selector)
}
