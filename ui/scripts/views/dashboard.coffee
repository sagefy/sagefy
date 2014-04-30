define([
    'jquery'
    'views/model'
    'hbs/sections/user/dashboard'
    'models/user'
], ($, ModelView, template, UserModel) ->

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
            @$el.addClass('max-width-8')
                .attr('id', 'dashboard')


)
