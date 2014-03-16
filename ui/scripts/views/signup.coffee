define([
    'jquery'
    'backbone'
    'hbs/sections/user/signup'
    'parsley'
], ($, Backbone, template, parsley) ->

    class Signup extends Backbone.View

        el: $('#page')
        template: template

        initialize: ->
            @render()

        render: ->
            document.title = 'Signup for Sagefy.'
            @$el.addClass('max-width-8')
                .attr('id', 'signup')
                .html(@template())

            @$el.find('form').parsley()


)
