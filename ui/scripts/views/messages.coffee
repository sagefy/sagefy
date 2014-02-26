define [
    'jquery'
    'backbone'
    'hbs/'
], ($, Bb, t) ->

    class MessagesView extends Bb.View

        el: $ {}

        initialize: ->
            @render()

        render: ->
