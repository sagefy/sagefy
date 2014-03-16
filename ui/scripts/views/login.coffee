define([
    'jquery'
    'backbone'
    'parsley'
    'hbs/sections/user/login'
], ($, Backbone, parsley, template) ->

    class LoginView extends Backbone.View

        el: $('#page')
        template: template

        initialize: ->
            @render()

        render: ->
            document.title = 'Login to Sagefy.'
            @$el.addClass('max-width-8')
                .attr('id', 'login')
                .html(@template())


)
