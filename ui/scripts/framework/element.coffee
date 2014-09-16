###
A miniature jQuery non-IE. Huzzah!
Borrowed from http://youmightnotneedjquery.com/
###

matches = (el, selector) ->
    return (el.matches ||
            el.matchesSelector ||
            el.msMatchesSelector ||
            el.mozMatchesSelector ||
            el.webkitMatchesSelector ||
            el.oMatchesSelector).call(el, selector)

class El
    constructor: (element) ->
        if element instanceof Array
            @_ = element
        if element instanceof Element
            @_ = [element]
        else if element instanceof NodeList
            @_ = Array::slice.apply(element)
        else if typeof element is 'string'
            @_ = Array::slice.apply(document.querySelectorAll(element))
        return this

    hide: ->
        _.style.display = 'none' for _ in @_
        return this

    show: ->
        _.style.display = '' for _ in @_
        return this

    addClass: (className) ->
        _.classList.add(className) for _ in @_
        return this

    removeClass: (className) ->
        _.classList.remove(className) for _ in @_
        return this

    hasClass: (className) ->
        for _ in @_
            if _.classList.contains(className)
                return true
        return false

    prepend: (el) ->
        _.insertBefore(el, _.firstChild) for _ in @_
        return this

    append: (el) ->
        _.appendChild(el) for _ in @_
        return this

    contains: (el) ->
        for _ in @_
            if typeof el is 'string' and _.querySelector(el) isnt null
                return true
            if el instanceof Element and _.contains(el)
                return true
        return false

    filter: (selector) ->
        return El(@_.filter((_) -> return matches(_, selector)))

    not: (selector) ->
        return El(@_.filter((_) -> return not matches(_, selector)))

    each: (fn) ->
        elements.forEach(@_, fn)
        return this

    empty: ->
        _.innerHTML = '' for _ in @_
        return this

    find: (selector) ->
        els = []
        for _ in @_
            els.concat(Array::slice.call(_.querySelectorAll(selector)))
        return El(els)

    parent: ->
        return El([_.parentNode for _ in @_])

    children: (selector) ->  # ???

    closest: (selector) ->  # ???

    attr: (key, value) ->
        if key instanceof Object
            for k, v of key
                @attr(k, v)
        else if not value
            if @_.length is 1
                return @_[0].getAttribute(key)
            else
                return [_.getAttribute(key) for _ in @_]
        else
            _.setAttribute(key, value) for _ in @_
        return this

    removeAttr: (key) ->
        _.removeAttribute(key) for _ in @_
        return this

    data: (key, value) ->
        return @attr('data-' + key, value)

    removeData: (key) ->
        return @removeAttr('data-' + key)

    html: (value) ->
        if value
            _.innerHTML = value for _ in @_
            return this
        return [_.innerHTML for _ in @_].join('')

    is: (selector) ->
        for _ in @_
            if matches(_, selector)
                return true
        return false

    remove: ->
        _.parentNode.removeChild(_) for _ in @_
        return null

    on: ->  # ???

    off: ->  # ???

    trigger: ->  # ???

    val: (value) ->  # ???

module.exports = El
