define [
    'jquery'
    'backbone'
    'hbs/'
], ($, Bb, t) ->

    class AccountView extends Bb.View

        el: $ {}

        initialize: ->
            @render()

        render: ->
