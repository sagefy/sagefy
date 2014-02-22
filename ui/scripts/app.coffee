require.config
    paths:
        jquery: 'jquery/dist/jquery'
        handlebars: 'handlebars/handlebars'
        underscore: 'underscore/underscore'
        backbone: 'backbone/backbone'
    shim:
        handlebars:
            exports: 'Handlebars'
            init: ->
                window.Handlebars = Handlebars
                window.Handlebars

require ['router'], (PrimaryRouter) ->
    primaryRouter = new PrimaryRouter
