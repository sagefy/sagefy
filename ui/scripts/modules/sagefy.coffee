Application = require('../framework/application')
MenuAdapter = require('../adapters/menu')
_ = require('../framework/utilities')

class Sagefy extends Application
    constructor: ->
        # Create the page container
        page = document.createElement('div')
        page.classList.add('page')
        document.body.appendChild(page)
        super
        @bindAdapter(MenuAdapter)
        @menu = new MenuAdapter()
        @bindLinks()

    remove: ->
        @menu.remove()
        super

    bindLinks: ->
        # When we click an internal link, use `navigate` instead
        document.body.addEventListener('click', (e) =>
            el = _.closest(e.target, document.body, 'a')
            if not el
                return

            # Navigate to in-app URLs instead of new page
            if el.matches('[href^="/"]')
                e.preventDefault()
                @navigate(el.pathname)
            # Do nothing on empty links
            else if el.matches('[href="#"]')
                e.preventDefault()
            # Open external URLs in new windows
            else if el.matches('[href*="//"]')
                el.target = '_blank'
        )

module.exports = Sagefy
