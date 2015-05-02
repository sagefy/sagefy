View = require('../../framework/view')
aux = require('../../modules/auxiliaries')

class SettingsPageView extends View
    constructor: ->
        super
        aux.setTitle('Settings')

module.exports = SettingsPageView
