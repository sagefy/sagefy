PageAdapter = require('./page')
template = require('../templates/pages/styleguide')
compiled = require('../templates/pages/compiled')

View = require('../framework/view')

class StyleguideAdapter extends PageAdapter
    url: '/styleguide'
    title: 'Style Guide and Component Library'
    # TODO: move copy to content directory

    render: ->
        super
        @view = new View({
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
