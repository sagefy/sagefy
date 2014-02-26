define [
    'jquery'
    'backbone'
    'hbs/'
], ($, Bb, t) ->

    class LoginView extends Bb.View

        el: $ {}

        initialize: ->
            @render()

        render: ->
