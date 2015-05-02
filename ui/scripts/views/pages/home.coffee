View = require('../../framework/view')
aux = require('../../modules/auxiliaries')

class HomePageView extends View
    id: 'home'
    className: 'col-8'
    template: require('../../templates/pages/home')

    constructor: ->
        super
        aux.setTitle('Open-Content Adaptive Learning Platform')
        # TODO localize
        @render()

module.exports = HomePageView
