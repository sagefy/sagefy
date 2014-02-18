require.config
    paths:
        jquery: 'jquery/dist/jquery'
        handlebars: 'handlebars/handlebars'
        _: 'underscore/underscore'
        backbone: 'backbone/backbone'
    shim:
        handlebars:
            exports: 'Handlebars'
            init: ->
                window.Handlebars = Handlebars
                window.Handlebars

require [
    'sections/styleguide'
]
