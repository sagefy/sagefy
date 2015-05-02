View = require('../../framework/view')
aux = require('../../modules/auxiliaries')

class TopicFormPageView extends View
    constructor: ->
        super
        title = (if @getTopicID() then 'Update' else 'Create') + ' a Topic'
        aux.setTitle(title)

module.exports = TopicFormPageView
