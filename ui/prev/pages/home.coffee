View = require('../../modules/view')
aux = require('../../modules/auxiliaries')

class HomePageView extends View

    template: require('./home.tmpl')

    constructor: ->
        super
        aux.setTitle('Open-Content Adaptive Learning Platform')
        # TODO localize
        @render()

module.exports = HomePageView
