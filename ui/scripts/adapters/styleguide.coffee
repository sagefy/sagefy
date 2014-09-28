PageAdapter = require('./page')
template = require('../templates/pages/styleguide')
compiled = require('../templates/pages/compiled')

StyleguideView = require('../views/pages/styleguide')

class StyleguideAdapter extends PageAdapter
    url: '/styleguide'
    title: 'Style Guide and Component Library'

    constructor: ->
        super
        @view = new StyleguideView({
            id: 'styleguide'
            className: 'col-10'
            template: template
            region: @page
        })
        @view.render({
            html: compiled
        })

    remove: ->
        @view.remove()
        super

module.exports = StyleguideAdapter
