define [
    'jquery'
    'backbone'
    'hbs/'
], ($, Bb, t) ->

    class CreateMessageView extends Bb.View

        el: $ {}

        initialize: ->
            @render()

        render: ->
