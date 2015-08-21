View = require('../../modules/view')
aux = require('../../modules/auxiliaries')

class StyleguidePageView extends View
    id: 'styleguide'
    className: 'col-10'
    template: require('./styleguide.tmpl')

    constructor: ->
        super
        aux.setTitle('Style Guide and Component Library')
        # TODO localize
        @render({
            html: require('./styleguide.compiled')
        })

module.exports = StyleguidePageView
