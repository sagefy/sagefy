Events = require('../framework/events')
_ = require('../framework/utilities')
MenuModel = require('../models/menu')
MenuView = require('../views/components/menu')

class MenuAdapter extends Events
    # There's no URL because it is omnipresent
    constructor: (options) ->
        super
        # Create the global menu
        @app = options.app
        @model = new MenuModel()
        @view = new MenuView({
            body: document.body
        })

        # When we update the model, update the view
        render = =>
            @view.render(@model.items())
        @listenTo(@model, 'changeState', render)
        render()

        # When we click an internal link, use `navigate` instead
        document.body.addEventListener('click', (e) =>
            el = _.closest(e.target, document.body, 'a[href^="/"]')
            if el
                e.preventDefault()
                @app.navigate(el.pathname)
        )

    remove: ->
        @view.remove()
        @model.remove()
        super

module.exports = MenuAdapter
