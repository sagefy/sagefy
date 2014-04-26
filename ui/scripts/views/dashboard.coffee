define([
    'jquery'
    'backbone'
    'hbs/sections/user/dashboard'
    'models/user'
], ($, Backbone, template, UserModel) ->

    class DashboardView extends Backbone.View

        el: $('.page')

        template: template

        initialize: ->
            @model = new UserModel({id: 'current'})
            @model.fetch()
            @model.on('sync', => @render)
            @model.on('error', ->
                Backbone.history.navigate('/login')
            )

        render: ->
            @$el.html(@template())
            @onRender()

        onRender: ->
            document.title = 'Welcome to your Dashboard'
            @$el.addClass('max-width-8')
                .attr('id', 'dashboard')


)
