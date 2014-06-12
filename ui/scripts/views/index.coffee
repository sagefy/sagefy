$ = require('jquery')
PageView = require('./page')
template = require('../../templates/sections/public/index')
mixins = require('../modules/mixins')

class IndexView extends PageView
    id: 'index'
    className: 'max-width-8'
    template: template
    title: 'Sagefy - Adaptive, collaborative, and open learning platform.'

    beforeRender: ->
        @templateData = {isLoggedIn: @isLoggedIn()}

    isLoggedIn: mixins.isLoggedIn

module.exports = IndexView
