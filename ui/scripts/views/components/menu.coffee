View = require('../../framework/view')
template = require('../../templates/components/menu')
itemTemplate = require('../../templates/components/menu_item')

# A menu component, creates an icon and on click, displays
# an iOS style list of options
class MenuView extends View
    className: 'menu'
    domEvents: {
        'click .menu__overlay': 'toggle'
        'click .menu__trigger': 'toggle'
        'click .menu__item a': 'select'
    }

    template: template
    itemTemplate: itemTemplate
    selected: false

    constructor: (options) ->
        super
        options.body.appendChild(@el)

    # Render the layout if needed
    # then render data
    render: (data) ->
        @el.innerHTML = @template()
        @renderItems(data)
        @delegateEvents()

    # Produces the data specific HTML
    renderItems: (data) ->
        # Reduce will automatically concat all the template
        # strings for the menu
        html = ''
        for item in data
            html += @itemTemplate(item)
        @el.querySelector('.menu__items').innerHTML = html

    # Open if closed, close if opened
    # Keeps track of own state
    toggle: (e) ->
        if e
            e.preventDefault()
            e.stopPropagation()
        @selected = ! @selected
        if @selected
            @el.classList.add('selected')
        else
            @el.classList.remove('selected')

    select: ->
        @toggle()

module.exports = MenuView
