$ = require('jquery')
ModelView = require('views/model')
template = require('hbs/sections/user/dashboard')
UserModel = require('models/user')
mixins = require('modules/mixins')

module.exports = class DashboardView extends ModelView
    el: $('.page')
    template: template

    beforeInitialize: ->
        @model = new UserModel({id: 'current'})
        @model.on('error', ->
            Backbone.history.navigate('/login')
        )

    onRender: ->
        document.title = 'Welcome to your Dashboard'
        @$el.attr('id', 'dashboard')
        @updatePageWidth(8)

    updatePageWidth: mixins.updatePageWidth

