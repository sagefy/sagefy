Events = require('../framework/events')
_ = require('../framework/utilities')
MenuModel = require('../models/menu')
MenuView = require('../views/components/menu')

class MenuAdapter extends Events
    # There's no URL because it is omnipresent
    constructor: (options) ->
        super
        # Create the global menu
        @model = new MenuModel()
        @view = new MenuView({
            body: document.body
        })

        # When we update the model, update the view
        render = =>
            @view.render(@model.items())
        @listenTo(@model, 'changeState', render)
        render()

    remove: ->
        @view.remove()
        @model.remove()
        super

module.exports = MenuAdapter
