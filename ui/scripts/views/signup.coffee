define([
    'jquery'
    'backbone'
    'hbs/sections/user/signup'
], ($, Bb, t) ->

    class Signup extends Bb.View

        el: $('#page')
        template: t

        initialize: ->
            @render()

        render: ->
            document.title = 'Signup for Sagefy.'
            @$el.addClass('max-width-8')
                .attr('id', 'signup')
                .html(@template())


)
