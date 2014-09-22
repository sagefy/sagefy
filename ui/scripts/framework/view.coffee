###
Views are responsible for:
- Create a DOM element to contain the view contents
- Rendering data
- Binding to content events
###

# TODO: Write tests

Events = require('./events')
require('./matches_polyfill')
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
            @el = document.createElement(@tagName or 'div')
            @el.setAttribute('id', @id) if @id
            @el.setAttribute('class', @className) if @className
            for attribute, value of @attributes or {}
                @el.setAttribute(attribute, value)
        return @el

    # Given data, renders it. If `template` is defined on the view,
    # the template function will be called and passed the data.
    # Overwrite liberally, keep `super`.
    render: (data) ->
        @data = data || {}
        if @el
            @el.innerHTML = if @template then @template(@data) else ''
        @delegateEvents()
        return this

    # Removes the element from the DOM in addition to
    # the regular remove capability.
    # Overwrite and `super` to clean up anything else.
    remove: ->
        @undelegateEvents()
        if @el.parentNode
            @el.parentNode.removeChild(@el)
        super

    # Takes `domEvents` and binds methods to events.
    delegateEvents: ->
        @undelegateEvents()
        for query, methodName of @domEvents or {}
            key = query.match(eventRegExp).slice(1)[0]
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
            [key, selector] = query.match(eventRegExp).slice(1)
            if key is e.type and e.target.matches(selector)
                @[methodName].call(this, e)


module.exports = View
