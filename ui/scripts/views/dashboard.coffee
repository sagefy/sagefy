Backbone = require('Backbone')
$ = require('jquery')
ModelView = require('../views/model')
template = require('../../templates/sections/user/dashboard')

class DashboardView extends ModelView
    id: 'dashboard'
    className: 'max-width-4'
    template: template

    beforeInitialize: ->
        @listenTo(@model, 'error', ->
            Backbone.history.navigate('/login')
        )

    onRender: ->
        document.title = 'Welcome to your Dashboard'

module.exports = DashboardView
