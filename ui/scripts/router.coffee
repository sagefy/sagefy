define [
    'backbone'
], (Bb) ->

    class PrimaryRouter extends Bb.Router

        routes:
            'styleguide': 'viewStyleguide'
            '(/)': 'viewIndex'

        initialize: ->
            Bb.history.start pushState: true

        viewIndex: ->
            require ['views/index'], (IndexView) ->
                indexView = new IndexView

        viewStyleguide: ->
            require ['views/styleguide'], (StyleguideView) ->
                styleguideView = new StyleguideView
