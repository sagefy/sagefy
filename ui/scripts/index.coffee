Application = require('./framework/application')

### TODO: This all needs to go somewhere else... ###
MenuModel = require('./models/menu')
MenuView = require('./views/menu')
class Sagefy extends Application
    constructor: ->
        # Create the page container
        page = document.createElement('div')
        page.classList.add('page')
        document.body.appendChild(page)

        super

        # Create the global menu
        @menuModel = new MenuModel()
        @menuView = new MenuView({
            region: document.body
        })

        # When we update the model, update the view
        render = ->
            @menuView.render(@model.items())
        @listenTo(@model, 'changeState', render)
        render()

        # When we click an internal link, use `navigate` instead
        document.body.addEventListener('click', (e) ->
            if e.target.matches('a[href^="/"]')
                e.preventDefault()
                href = e.target.getAttribute('href')
                @navigate(href)
        )

$(->
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
