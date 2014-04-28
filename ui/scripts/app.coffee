require.config({
    paths: {
        jquery:
            'bower/jquery/dist/jquery'
        'jquery.cookie':
            'bower/jquery.cookie/jquery.cookie'
        handlebars:
            'bower/handlebars/handlebars'
        underscore:
            'bower/underscore/underscore'
        backbone:
            'bower/backbone/backbone'
        marionette:
            'bower/marionette/lib/backbone.marionette'
        "backbone.wreqr":
            'bower/backbone.wreqr/lib/backbone.wreqr'
        "backbone.babysitter":
            'bower/backbone.babysitter/lib/backbone.babysitter'
        markdown:
            'bower/marked/lib/marked'
        moment:
            'bower/moment/moment'
        d3:
            'bower/d3/d3'
        modernizr:
            'bower/modernizr/modernizr'
    }
    shim: {
        jquery: {
            exports: 'jQuery'
        }
        handlebars: {
            exports: 'Handlebars'
            init: ->
                window.Handlebars = Handlebars
        }
        underscore: {
            exports: '_'
        }
        backbone: {
            deps: ['jquery', 'underscore']
            exports: 'Backbone'
        }
        marionette: {
            deps: ['jquery', 'underscore', 'backbone']
            exports: 'Marionette'
        }
    }
})

require([
    'router'
    'modules/hbs_helpers'
    'jquery.cookie'
], (PrimaryRouter) ->
    primaryRouter = new PrimaryRouter()
)
