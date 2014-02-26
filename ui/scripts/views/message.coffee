define [
    'jquery'
    'backbone'
    'hbs/'
], ($, Bb, t) ->

    class MessageView extends Bb.View

        el: $ {}

        initialize: ->
            @render()

        render: ->
