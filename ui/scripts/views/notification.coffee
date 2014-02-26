define [
    'jquery'
    'backbone'
    'hbs/'
], ($, Bb, t) ->

    class NotificationView extends Bb.View

        el: $ {}

        initialize: ->
            @render()

        render: ->
