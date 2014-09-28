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
            el = _.closest(e.target, document.body, 'a')
            if not el
                return

            # Navigate to in-app URLs instead of new page
            if el.matches('[href^="/"]')
                e.preventDefault()
                @app.navigate(el.pathname)
            # Do nothing on empty links
            else if el.matches('[href="#"]')
                e.preventDefault()
            # Open external URLs in new windows
            else if el.matches('[href*="//"]')
                el.target = '_blank'
        )

    remove: ->
        @view.remove()
        @model.remove()
        super

module.exports = MenuAdapter
