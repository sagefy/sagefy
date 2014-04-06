define([
    'jquery'
    'backbone'
    'hbs/sections/user/dashboard'
    'models/user'
], ($, Backbone, template, UserModel) ->

    class DashboardView extends Backbone.View

        el: $('.page')

        initialize: ->
            @model = new UserModel({id: 'current/'})
            @model.fetch()
            @render()

        render: ->
            @$el.html(@template())
            @onRender()

        onRender: ->
            document.title = 'Welcome to your Dashboard'
            @$el.addClass('max-width-8')
                .attr('id', 'dashboard')


)
