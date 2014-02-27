define [
    'jquery'
    'backbone'
    'hbs/'
], ($, Bb, t) ->

    class AccountView extends Bb.View

        el: $ '#page'

        initialize: ->
            @render()

        render: ->
