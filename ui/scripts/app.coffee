require.config({
    paths: {
        jquery: 'bower/jquery/dist/jquery'
        handlebars: 'bower/handlebars/handlebars'
        underscore: 'bower/underscore/underscore'
        backbone: 'bower/backbone/backbone'
        markdown: 'bower/marked/marked'
        moment: 'bower/moment/moment'
        d3: 'bower/d3/d3'
        modernizr: 'bower/modernizr/modernizr'
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
