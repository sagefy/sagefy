require('matches_polyfill')
diff = require('virtual-dom/diff')
patch = require('virtual-dom/patch')
createElement = require('virtual-dom/create-element')

eventRegExp = /^(\S+) (.*)$/

store = {
    data: window.preload or {}
    actions: {}

    init: (fn) ->
        fn.call(this)

    add: (obj) ->
        for key, value of obj
            @actions[key] = value
        return obj

    bind: (fn) ->
        return @callback = fn

    change: ->
        return @callback(@data)
}

store.init(->
    prev = window.onpopstate if window.onpopstate
    window.onpopstate = (event) =>
        prev(event) if prev
        @data.route = window.location.pathname
    @data.route = window.location.pathname
)

store.add({
    route: (path) ->
        if path isnt window.location.pathname
            history.pushState({}, '', path)
})

broker = {
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

init = (options) ->
    {view, el} = options

    tree = view(store.data)
    root = createElement(tree)
    el.appendChild(root)

    store.bind((data) ->
        next = view(data)
        root = patch(root, diff(tree, next))
        tree = next
    )

    broker.el = el
    for type in ['click', 'change', 'keydown', 'submit']
        @events[type] = {}
        el.addEventListener(type, @delegate(type))

module.exports = {init, store, broker}
