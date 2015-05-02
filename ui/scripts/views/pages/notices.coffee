View = require('../../framework/view')
aux = require('../../modules/auxiliaries')

class NoticesPageView extends View
    constructor: ->
        super
        aux.setTitle('Notices')

module.exports = NoticesPageView
