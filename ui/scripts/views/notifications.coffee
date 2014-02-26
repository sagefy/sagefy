define [
    'jquery'
    'backbone'
    'hbs/'
], ($, Bb, t) ->

    class NotificationsView extends Bb.View

        el: $ {}

        initialize: ->
            @render()

        render: ->
