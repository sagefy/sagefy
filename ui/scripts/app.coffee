require.config
    paths:
        jquery: 'bower/jquery/dist/jquery'
        handlebars: 'bower/handlebars/handlebars'
        underscore: 'bower/underscore/underscore'
        backbone: 'bower/backbone/backbone'
    shim:
        handlebars:
            exports: 'Handlebars'
            init: ->
                window.Handlebars = Handlebars
                window.Handlebars

require ['router'], (PrimaryRouter) ->
    primaryRouter = new PrimaryRouter
