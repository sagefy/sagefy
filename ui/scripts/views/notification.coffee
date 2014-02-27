define [
    'jquery'
    'backbone'
    'hbs/'
], ($, Bb, t) ->

    class NotificationView extends Bb.View

        el: $ '#page'

        initialize: ->
            @render()

        render: ->
