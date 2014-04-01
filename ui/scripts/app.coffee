require.config({
    paths: {
        jquery: 'bower/jquery/dist/jquery'
        handlebars: 'bower/handlebars/handlebars'
        underscore: 'bower/underscore/underscore'
        backbone: 'bower/backbone/backbone'
        "backbone.wreqr": 'bower/backbone.wreqr/lib/backbone.wreqr'
        "backbone.babysitter": 'bower/backbone.babysitter/lib/backbone.babysitter'
        "backbone.marionette": 'bower/marionette/lib/core/amd/backbone.marionette'
        markdown: 'bower/marked/lib/marked'
        moment: 'bower/moment/moment'
        d3: 'bower/d3/d3'
        modernizr: 'bower/modernizr/modernizr'
        validation: 'bower/jquery-validation/jquery.validate'
    }
    shim: {
        handlebars: {
            exports: 'Handlebars'
            init: ->
                window.Handlebars = Handlebars
        }
    }
})

require([
    'router'
    'modules/hbs_helpers'
], (PrimaryRouter) ->
    primaryRouter = new PrimaryRouter()
)
