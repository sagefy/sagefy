$ = require('jquery')
Backbone = require('backbone')
Backbone.$ = $
_ = require('underscore')
layoutTemplate = require('../../templates/components/menu/layout')
itemTemplate = require('../../templates/components/menu/item')

# A menu component, creates an icon and on click, displays
# an iOS style list of options
class MenuView extends Backbone.View
    className: 'menu'
    events: {
        'click .menu__overlay': 'toggle'
        'click .menu__trigger': 'toggle'
        'click .menu__item a': 'select'
    }

    layoutTemplate: layoutTemplate
    itemTemplate: itemTemplate
    selected: false

    initialize: (options) ->
        @model ||= options.model
        @$region = options.$region
        # When we update the model, update the view
        @listenTo(@model, 'changeState', @render)
        @render()

    # Render the layout if needed
    # then render the state of the model
    render: ->
        if ! @$layout
            @renderLayout()
        @renderItems()

    # Produces the basic HTML for the menu
    renderLayout: ->
        @$el.html(@layoutTemplate())
        @$items = @$el.find('.menu__items')
        @$region.prepend(@$el)

    # Produces the model specific HTML
    renderItems: ->
        # Reduce will automatically concat all the template
        # strings for the menu
        html = _.reduce(@model.items(), (memo, item) =>
            return memo + @itemTemplate(item)
        , '')

        @$items.html(html)

    # Open if closed, close if opened
    # Keeps track of own state
    toggle: (e) ->
        if e
            e.preventDefault()
            e.stopPropagation()
        @selected = ! @selected
        @$el.toggleClass('selected', @selected)

    select: ->
        @toggle()

module.exports = MenuView
