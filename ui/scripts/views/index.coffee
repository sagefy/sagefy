define([
    'jquery'
    'backbone'
    'hbs/sections/public/index'
    'modules/mixins'
], ($, Bb, t, mixins) ->

    class IndexView extends Bb.View

        el: $('.page')
        template: t

        initialize: ->
            @render()

        render: ->
            document.title = 'Sagefy - ' +
                'Adaptive, collaborative, and open learning platform.'
            @$el.attr('id', 'index')
                .html(@template({isLoggedIn: @isLoggedIn()}))
            @updatePageWidth(8)

        updatePageWidth: mixins.updatePageWidth
        isLoggedIn: mixins.isLoggedIn


)
