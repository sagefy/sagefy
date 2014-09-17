###
TODO:
- Write description
- Write tests
- Write delegate and undelegate events
- Naive templating system
###

Events = require('./events')

class View extends Events
    id: ''
    className: ''
    tagName: 'div'
    attributes: {}
    el: null
    region: null
    domEvents: {}
    template: null

    setElement: (element) ->
        if element
            @el = element
        else
            @el = document.createElement(@tagName)
            @el.setAttribute('id', @id)
            @el.setAttribute('class', @className)
            for attribute, value of attributes
                @el.setAttribute(attribute, value)
        return @el

    render: (data) ->
        @data = data || {}
        if @el
            @el.html(if @template then @template(@data) else '')
        return this

    remove: ->
        if @el.parentNode
            @el.parentNode.removeChild(@el)
        super()

    delegateEvents: ->

        return this

    undelegateEvents: ->

        return this

module.exports = View
