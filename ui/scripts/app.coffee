require.config({
    paths: {
        jquery:
            'bower/jquery/dist/jquery'
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
        validation:
            'bower/jquery-validation/jquery.validate'
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
        validation: {
            deps: ['jquery']
        }
    }
})

require([
    'router'
    'modules/hbs_helpers'
], (PrimaryRouter) ->
    primaryRouter = new PrimaryRouter()
)
