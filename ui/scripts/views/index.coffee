$ = require('jquery')
Backbone = require('backbone')
template = require('../../templates/sections/public/index')
mixins = require('../modules/mixins')

class IndexView extends Backbone.View
    id: 'index'
    className: 'max-width-8'
    template: template

    initialize: (options) ->
        @$region = options.$region
        @render()

    render: ->
        document.title = 'Sagefy - ' +
            'Adaptive, collaborative, and open learning platform.'
        @$el.html(@template({isLoggedIn: @isLoggedIn()}))
        @$region.html(@$el)

    isLoggedIn: mixins.isLoggedIn

module.exports = IndexView
