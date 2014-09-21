###
A view which contains a list of other views.
###

View = require('./view')

class ListView extends View
    constructor: ->
        super
        @views = []

    render: ->
        super

module.exports = ListView
