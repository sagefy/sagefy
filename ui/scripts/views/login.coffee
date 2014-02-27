define [
    'jquery'
    'backbone'
    'hbs/sections/user/login'
], ($, Bb, t) ->

    class LoginView extends Bb.View

        el: $ '#page'
        template: t

        initialize: ->
            @render()

        render: ->
            document.title = 'Login to Sagefy.'
            @$el.addClass 'max-width-8'
                .attr 'id', 'login'
                .html @template()
