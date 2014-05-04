define([
    'jquery'
    'views/model'
    'hbs/sections/user/dashboard'
    'models/user'
    'modules/mixins'
], ($, ModelView, template, UserModel, mixins) ->

    class DashboardView extends ModelView

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


)
