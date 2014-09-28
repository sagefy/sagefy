Application = require('./framework/application')
MenuAdapter = require('./adapters/menu')

class Sagefy extends Application
    constructor: ->
        # Create the page container
        page = document.createElement('div')
        page.classList.add('page')
        document.body.appendChild(page)
        super
        @menu = new MenuAdapter({app: this})


    remove: ->
        @menu.remove()
        super

document.addEventListener('DOMContentLoaded', ->
    app = new Sagefy(
        require('./adapters/signup')
        require('./adapters/login')
        require('./adapters/logout')
        require('./adapters/password')
        require('./adapters/styleguide')
        require('./adapters/terms')
        require('./adapters/contact')
        require('./adapters/settings')
        require('./adapters/index')
        require('./adapters/error')
    )
    app.route(window.location.pathname)
)
