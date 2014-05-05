$ = require('jquery')
Bb = require('backbone')
t = require('hbs/sections/public/index')
mixins = require('modules/mixins')

module.exports = class IndexView extends Bb.View
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
