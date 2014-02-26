define [
    'jquery'
    'backbone'
    'hbs/'
], ($, Bb, t) ->

    class PasswordView extends Bb.View

        el: $ {}

        initialize: ->
            @render()

        render: ->
