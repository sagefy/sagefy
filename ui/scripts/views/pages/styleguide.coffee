View = require('../../framework/view')
aux = require('../../modules/auxiliaries')

class StyleguidePageView extends View
    id: 'styleguide'
    className: 'col-10'
    template: require('../../templates/pages/styleguide')

    constructor: ->
        super
        aux.setTitle('Style Guide and Component Library')
        # TODO localize
        @render({
            html: require('../../templates/pages/compiled')
        })

module.exports = StyleguidePageView
