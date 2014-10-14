###
Views are responsible for:
- Create a DOM element to contain the view contents
- Rendering data
- Binding to content events
###

Events = require('./events')
_ = require('./utilities')
eventRegExp = /^(\S+) (.*)$/

class View extends Events
    # On creating a new view, create the element and possibly set the region
    constructor: ->
        super
        @setElement(@options.element)
        @setRegion(@options.region) if @options.region
        @template = @options.template if @options.template
        @myDelegatedEvent = @delegatedEvent.bind(this)

    # Places the element inside of the provided region
    setRegion: (@region) ->
        @region.innerHTML = ''
        @region.appendChild(@el)

    # Create the containing DOM element, based on
    # instance properties `id`, `className`, `tagName`, and `attributes`.
    # Can also receive a DOM element directly.
    setElement: (element) ->
        if element
            @el = element
        else
            @el = @createElement({
                tagName: @options.tagName or @tagName
                id: @options.id or @id
                className: @options.className or @className
                attributes: @options.attributes or @attributes
            })
        return @el

    # Create a DOM element, based on options
    # `id`, `className`, `tagName`, and `attributes`
    createElement: (options) ->
        el = document.createElement(options.tagName or 'div')
        if options.id
            el.id = options.id
        if options.className
            el.className = options.className
        for attribute, value of options.attributes or {}
            el.setAttribute(attribute, value)
        return el

    # Given data, renders it. If `template` is defined on the view,
    # the template function will be called and passed the data.
    # Overwrite liberally, keep `super`.
    render: (data) ->
        @data = data || {}
        if @el
            @el.innerHTML = if @template then @template(@data) else ''
        @selectElements()
        @delegateEvents()
        return this

    # If the user has entered `elements` on the view
    # in a `key: selector` hash,
    # we will go ahead and select those elements at store them at key
    selectElements: ->
        for key, selector of @elements or {}
            @[key] = @el.querySelectorAll(selector)
            if @[key].length is 1
                @[key] = @[key][0]

    # Remove all elements stored as a result of `selectElements`
    unselectElements: ->
        for key in Object.keys(@elements or {})
            delete @[key]

    # Removes the element from the DOM in addition to
    # the regular remove capability.
    # Overwrite and `super` to clean up anything else.
    remove: ->
        @undelegateEvents()
        @unselectElements()
        if @el.parentNode
            @el.parentNode.removeChild(@el)
        super

    # Takes `domEvents` and binds methods to events.
    delegateEvents: ->
        @undelegateEvents()
        for query, methodName of @domEvents or {}
            match = query.match(eventRegExp)
            key = if match then match.slice(1)[0] else query
            @domEventKeys.push(key)
        for key in @domEventKeys
            @el.addEventListener(key, @myDelegatedEvent)
        return this

    # Clears all events in `domEvents`
    undelegateEvents: ->
        for key in @domEventKeys or []
            @el.removeEventListener(key, @myDelegatedEvent)
        @domEventKeys = []
        return this

    # Looks through the events, and calls any matching functions
    delegatedEvent: (e) ->
        for query, methodName of @domEvents or {}
            match = query.match(eventRegExp)
            if match
                [key, selector] = match.slice(1)
            else
                key = match
            if (not selector) or
               (key is e.type and _.closest(e.target, @el, selector))
                @[methodName].call(this, e)

module.exports = View
