define [
    'jquery'
    'backbone'
    'hbs/'
], ($, Bb, t) ->

    class SignupView extends Bb.View

        el: $ {}

        initialize: ->
            @render()

        render: ->
