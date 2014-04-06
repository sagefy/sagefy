define([
    'jquery'
    'backbone'
    'hbs/sections/user/signup'
    'models/user'
    'modules/mixins'
], ($, Backbone, template, UserModel, mixins) ->

    class Signup extends Backbone.View

        el: $('.page')
        template: template
        events: {
            'submit form': 'submit'
        }

        initialize: ->
            if @isLoggedIn()
                Backbone.history.navigate('/dashboard')
            @model = new UserModel()
            @render()

        render: ->
            @$el.html(@template())
            @onRender()

        onRender: ->
            document.title = 'Signup for Sagefy.'
            @$el.addClass('max-width-8')
                .attr('id', 'signup')
            @$form = @$el.find('form')
            @$form.validate(@model.fields)

        submit: (e) ->
            e.preventDefault()
            @model.save(@formData(@$form))
            @model.on('sync', ->
                window.location = '/dashboard'
                # Hard redirect to get the cookie
            )

        formData: mixins.formData
        isLoggedIn: mixins.isLoggedIn


)
