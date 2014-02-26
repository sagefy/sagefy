define [
    'jquery'
    'backbone'
    'hbs/'
], ($, Bb, t) ->

    class MenuView extends Bb.View

        el: $ {}

        initialize: ->
            @render()

        render: ->
