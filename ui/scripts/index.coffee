$ = require('jquery')
Backbone = require('backbone')
Backbone.$ = $
Handlebars = require('hbsfy/runtime')
hbsHelpers = require('./modules/hbs_helpers')(Handlebars)
Application = require('./framework/application')

### TODO: This all needs to go somewhere else... ###
MenuModel = require('./models/menu')
MenuView = require('./views/menu')
class Sagefy extends Application
    constructor: ->
        # Create the page container
        $region = $('body')
        $region.prepend('<div class="page"></div>')

        super

        # Create the global menu
        @menuModel = new MenuModel()
        @menuView = new MenuView({
            $region: $region
            model: @menuModel
        })

        # When we click an internal link, use Navigate instead
        $region.on('click', 'a[href^="/"]', (e) =>
            e.preventDefault()
            href = $(e.currentTarget).closest('a').attr('href')
            @navigate(href, {trigger: true})
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
