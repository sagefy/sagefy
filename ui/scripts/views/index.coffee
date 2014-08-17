$ = require('jquery')
PageView = require('./page')
template = require('../../templates/sections/public/index')
mixins = require('../modules/mixins')

class IndexView extends PageView
    id: 'index'
    className: 'col-8'
    template: template
    title: 'Adaptive, Collaborative, and Open Learning Platform'

    render: ->
        @templateData = {isLoggedIn: @isLoggedIn()}
        super()

    isLoggedIn: mixins.isLoggedIn

module.exports = IndexView
