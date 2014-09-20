###
Views are responsible for:
- Create a DOM element to contain the view contents
- Rendering data
- Binding to content events
###

# TODO: Write tests

Events = require('./events')
require('./matches_polyfill')

class View extends Events
    # On creating a new view, create the element and possibly set the region
    constructor: ->
        super
        @setElement(@options.element)
        @setRegion(@options.region)

    # Places the element inside of the provided region
    setRegion: (@region) ->
        @region.appendChild(@el) if @region

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
            for attribute, value of attributes or {}
                @el.setAttribute(attribute, value)
        return @el

    # Given data, renders it. If `template` is defined on the view,
    # the template function will be called and passed the data.
    # Overwrite liberally, keep `super`.
    render: (data) ->
        @data = data || {}
        @el.html(if @template then @template(@data) else '') if @el
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
            [key, selector] = query.match(/^(\S+) (.*)$/).slice(1)
            @refDomEvents[key] = (e) ->
                if e.target.matches(selector)
                    @[methodName].call(this, e)
            @el.addEventListener(key, @refDomEvents[key])
        return this

    # Clears all events in `refDomEvents`
    undelegateEvents: ->
        for key, method of @refDomEvents or {}
            @el.removeEventListener(key, method)
        @refDomEvents = {}
        return this

module.exports = View
